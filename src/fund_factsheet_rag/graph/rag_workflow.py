"""
LangGraph-based RAG workflow for Fund Factsheet Chatbot
Implements stateful conversation flow with retrieval, memory, and generation
"""
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain.schema import Document, HumanMessage, AIMessage, BaseMessage
import operator
from ..indexer.vector_store import similarity_search
from ..llm.qa_generator import generate_answer
from ..calculations.finance import calculate_cagr, parse_numeric_value
from ..memory.conversation_memory import get_memory_manager
import re

# Define the state structure
class RAGState(TypedDict):
    """State for the RAG workflow with memory"""
    question: str
    retrieved_docs: list
    answer: str
    sources: list
    needs_calculation: bool
    calculation_result: str
    chat_history: Annotated[Sequence[BaseMessage], operator.add]
    conversation_context: str
    memory_used: bool
    error: str

# Node functions
def load_memory(state: RAGState) -> RAGState:
    """
    Load relevant conversation history from memory
    """
    question = state["question"]

    try:
        memory_manager = get_memory_manager()

        # Get conversation context (recent + relevant)
        context = memory_manager.get_conversation_context(
            query=question,
            include_recent=3,
            include_relevant=2
        )

        state["conversation_context"] = context
        state["memory_used"] = bool(context)

    except Exception as e:
        state["conversation_context"] = ""
        state["memory_used"] = False
        print(f"Memory load error: {e}")

    return state

def retrieve_documents(state: RAGState) -> RAGState:
    """
    Retrieve relevant documents from FAISS vector store
    Uses conversation context if available
    Results are sorted by similarity in descending order (most similar first)
    Duplicates are filtered out based on document content
    """
    question = state["question"]
    context = state.get("conversation_context", "")

    try:
        # Enhance query with context if available
        enhanced_query = question
        if context:
            enhanced_query = f"{context}\n\nCurrent question: {question}"

        # Perform similarity search (get more results to filter duplicates)
        results = similarity_search(question, k=10)  # Get more results to filter duplicates

        # Sort results by similarity in descending order (most similar first)
        # FAISS returns (doc, distance) where lower distance = more similar
        # Convert to similarity and sort descending
        sorted_results = sorted(
            results,
            key=lambda x: 1.0 / (1.0 + float(x[1])),  # Convert distance to similarity
            reverse=True  # Descending order (highest similarity first)
        )

        # Filter duplicates based on document content (use hash for exact duplicates)
        import hashlib
        seen_content_hashes = set()
        unique_results = []
        for doc, score in sorted_results:
            # Normalize content and create hash
            content_normalized = doc.page_content.strip()
            content_hash = hashlib.md5(content_normalized.encode('utf-8')).hexdigest()
            
            # Include page and type to allow same content on different pages
            page = doc.metadata.get('page', 'unknown')
            doc_type = doc.metadata.get('type', 'text')
            unique_key = f"{content_hash}__page_{page}__type_{doc_type}"
            
            if unique_key not in seen_content_hashes:
                seen_content_hashes.add(unique_key)
                unique_results.append((doc, score))
                # Stop when we have enough unique results
                if len(unique_results) >= 5:
                    break

        state["retrieved_docs"] = unique_results
        state["error"] = ""
    except Exception as e:
        state["retrieved_docs"] = []
        state["error"] = f"Retrieval error: {str(e)}"

    return state

def check_calculation_needed(state: RAGState) -> RAGState:
    """
    Determine if the question requires financial calculations
    """
    question = state["question"].lower()

    # Keywords that suggest calculation is needed
    calc_keywords = [
        "calculate", "cagr", "average", "return", "compare",
        "difference", "percentage", "ratio", "growth rate"
    ]

    needs_calc = any(keyword in question for keyword in calc_keywords)
    state["needs_calculation"] = needs_calc

    return state

def perform_calculation(state: RAGState) -> RAGState:
    """
    Perform financial calculations if needed
    """
    if not state["needs_calculation"]:
        state["calculation_result"] = ""
        return state

    question = state["question"].lower()
    retrieved_docs = state["retrieved_docs"]

    try:
        # Extract numerical data from retrieved documents
        doc_text = " ".join([doc.page_content for doc, _ in retrieved_docs])

        # Try to calculate CAGR if mentioned
        if "cagr" in question:
            # Simple pattern matching for demo - in production, use more sophisticated NLP
            numbers = re.findall(r'(\d+\.?\d*)%', doc_text)
            if len(numbers) >= 2:
                result = f"Calculation based on data: {numbers}"
                state["calculation_result"] = result
            else:
                state["calculation_result"] = "Insufficient data for CAGR calculation"
        else:
            state["calculation_result"] = ""

    except Exception as e:
        state["calculation_result"] = f"Calculation error: {str(e)}"

    return state

def generate_response(state: RAGState) -> RAGState:
    """
    Generate answer using Groq LLM and save to memory
    """
    question = state["question"]
    retrieved_docs = state["retrieved_docs"]
    calc_result = state.get("calculation_result", "")
    context = state.get("conversation_context", "")

    try:
        # Generate answer
        result = generate_answer(question, retrieved_docs, source_info=True)

        # Append calculation result if available
        if calc_result:
            result["answer"] = f"{result['answer']}\n\nCalculation: {calc_result}"

        state["answer"] = result["answer"]
        state["sources"] = result["sources"]
        state["error"] = ""

        # Save to memory
        try:
            memory_manager = get_memory_manager()
            memory_manager.add_conversation_turn(
                user_message=question,
                assistant_message=result["answer"],
                metadata={
                    "sources_count": len(result["sources"]),
                    "had_calculation": bool(calc_result)
                }
            )
        except Exception as mem_error:
            print(f"Error saving to memory: {mem_error}")

    except Exception as e:
        state["answer"] = f"Error generating answer: {str(e)}"
        state["sources"] = []
        state["error"] = str(e)

    return state

def route_after_retrieval(state: RAGState) -> str:
    """
    Routing function: decide next step after retrieval
    """
    if state.get("error"):
        return "generate"  # Go straight to generation to report error

    if not state["retrieved_docs"]:
        return "generate"  # No docs found, generate "not found" response

    return "check_calculation"

def route_after_check(state: RAGState) -> str:
    """
    Routing function: decide if calculation is needed
    """
    if state.get("needs_calculation", False):
        return "calculate"
    return "generate"

# Build the workflow graph
def create_rag_workflow():
    """
    Create and compile the LangGraph RAG workflow with memory
    """
    workflow = StateGraph(RAGState)

    # Add nodes (memory first!)
    workflow.add_node("load_memory", load_memory)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("check_calculation", check_calculation_needed)
    workflow.add_node("calculate", perform_calculation)
    workflow.add_node("generate", generate_response)

    # Set entry point to memory
    workflow.set_entry_point("load_memory")

    # Add edge from memory to retrieve
    workflow.add_edge("load_memory", "retrieve")

    # Add conditional edges
    workflow.add_conditional_edges(
        "retrieve",
        route_after_retrieval,
        {
            "check_calculation": "check_calculation",
            "generate": "generate"
        }
    )

    workflow.add_conditional_edges(
        "check_calculation",
        route_after_check,
        {
            "calculate": "calculate",
            "generate": "generate"
        }
    )

    # Add edge from calculate to generate
    workflow.add_edge("calculate", "generate")

    # Add edge from generate to END
    workflow.add_edge("generate", END)

    # Compile the workflow
    app = workflow.compile()

    return app

# Convenience function to run the workflow
def run_rag_query(question: str, chat_history: list = None) -> dict:
    """
    Run a query through the RAG workflow

    Args:
        question: User's question
        chat_history: Optional chat history for context

    Returns:
        dict with answer, sources, and metadata
    """
    if chat_history is None:
        chat_history = []

    # Create initial state with memory fields
    initial_state = {
        "question": question,
        "retrieved_docs": [],
        "answer": "",
        "sources": [],
        "needs_calculation": False,
        "calculation_result": "",
        "chat_history": chat_history,
        "conversation_context": "",
        "memory_used": False,
        "error": ""
    }

    # Create and run workflow
    app = create_rag_workflow()
    result = app.invoke(initial_state)

    # Extract final result
    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": result["sources"],
        "calculation_performed": bool(result.get("calculation_result")),
        "memory_used": result.get("memory_used", False),
        "error": result.get("error", "")
    }
