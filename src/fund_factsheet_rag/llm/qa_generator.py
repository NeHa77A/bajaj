"""
Groq-based LLM module using LangChain
"""
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

_llm = None

def get_llm():
    """Get or create Groq LLM instance"""
    global _llm
    if _llm is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        _llm = ChatGroq(
            groq_api_key=api_key,
            model_name=CFG["models"]["groq_model"],
            temperature=CFG["models"]["temperature"],
            max_tokens=CFG["models"]["max_tokens"]
        )
    return _llm

def generate_answer(user_query: str, retrieved_docs: list, source_info: bool = True) -> dict:
    """
    Generate natural language answers using retrieved PDF context with Groq.

    Args:
        user_query: User's question
        retrieved_docs: List of tuples (Document, score) from FAISS search
        source_info: Whether to include source information

    Returns:
        dict with 'answer' and 'sources'
    """
    if not retrieved_docs:
        return {
            "answer": "I couldn't find relevant information in the factsheet to answer your question. Please try rephrasing or ask something else about the fund data.",
            "sources": []
        }

    # Extract documents and prepare context
    docs = [doc for doc, score in retrieved_docs]
    context_parts = []
    sources = []

    for idx, (doc, distance) in enumerate(retrieved_docs):
        # Convert FAISS distance to similarity score (higher = more similar)
        similarity = 1.0 / (1.0 + float(distance))
        
        context_parts.append(f"[Source {idx+1}]\n{doc.page_content}\n")
        sources.append({
            "source_id": idx + 1,
            "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
            "metadata": doc.metadata,
            "score": similarity  # Use similarity score (higher = more similar)
        })

    context = "\n".join(context_parts)

    # Create prompt
    system_prompt = """You are an expert financial analyst assistant specialized in mutual fund factsheets.
Your role is to:
1. Answer questions accurately using ONLY the information provided in the context
2. Perform calculations when needed (CAGR, returns, allocations, etc.)
3. Cite sources using [Source N] notation
4. If information is not in the context, clearly state that
5. Be precise with numbers and percentages
6. Format your response clearly"""

    human_prompt = f"""Context from Fund Factsheet:
{context}

Question: {user_query}

Please provide a clear, accurate answer based on the context above. If you perform any calculations, show your work."""

    llm = get_llm()

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    # Generate response
    response = llm.invoke(messages)
    answer = response.content

    return {
        "answer": answer,
        "sources": sources if source_info else []
    }

def generate_answer_with_chain(user_query: str, retrieved_docs: list) -> dict:
    """
    Alternative implementation using LangChain LCEL (LangChain Expression Language)
    """
    from langchain.schema.runnable import RunnablePassthrough
    from langchain.schema.output_parser import StrOutputParser

    if not retrieved_docs:
        return {
            "answer": "No relevant information found in the documents.",
            "sources": []
        }

    # Format context
    docs = [doc for doc, score in retrieved_docs]
    context = "\n\n".join([f"Source {i+1}:\n{doc.page_content}" for i, (doc, score) in enumerate(retrieved_docs)])

    # Create prompt template
    template = """You are an expert financial analyst. Answer the question based on the following context from fund factsheets.

Context:
{context}

Question: {question}

Answer clearly and cite sources when relevant:"""

    prompt = ChatPromptTemplate.from_template(template)
    llm = get_llm()

    # Create chain
    chain = (
        {"context": lambda x: context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(user_query)

    sources = [
        {
            "source_id": idx + 1,
            "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
            "metadata": doc.metadata,
            "score": float(score)
        }
        for idx, (doc, score) in enumerate(retrieved_docs)
    ]

    return {
        "answer": answer,
        "sources": sources
    }
