"""
Enhanced Streamlit UI for Fund Factsheet RAG Chatbot
Using LangChain, LangGraph, FAISS, and Groq
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.fund_factsheet_rag.graph.rag_workflow import run_rag_query
from src.fund_factsheet_rag.indexer.vector_store import get_vector_store
from src.fund_factsheet_rag.memory.conversation_memory import get_memory_manager
import yaml

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

# Page configuration
st.set_page_config(
    page_title="Bajaj AMC Factsheet Chatbot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .assistant-message {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .source-box {
        background-color: #fff3cd;
        padding: 0.8rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.markdown("### 💼 Fund Factsheet RAG")
    st.markdown("---")

    st.markdown("#### ⚙️ Configuration")
    st.info(f"""
    **Model:** {CFG['models']['groq_model']}
    **Embedding:** {CFG['models']['text_embedding'].split('/')[-1]}
    """)

    st.markdown("---")
    st.markdown("#### 📝 Sample Questions")

    sample_questions = [
        "What is the 3-year return of Bajaj Flexi Cap Fund?",
        "List top 5 holdings of the Consumption Fund with weights",
        "Compare the allocation between equity and debt",
        "How has AUM changed compared to last month?",
        "Which equity fund has the highest 3-year return?",
        "State the YTM and Macaulay Duration for the Money Market Fund"
    ]

    for i, question in enumerate(sample_questions):
        if st.button(question, key=f"sample_{i}"):
            st.session_state.current_question = question

    st.markdown("---")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        # Also clear memory
        try:
            memory_manager = get_memory_manager()
            memory_manager.clear_memory()
            st.success("Chat history and memory cleared!")
        except Exception as e:
            st.warning(f"Chat cleared but memory clear failed: {e}")
        st.rerun()

    st.markdown("---")
    st.markdown("#### 📊 About")
    st.markdown("""
    This chatbot uses:
    - **LangChain** for document processing
    - **LangGraph** for workflow orchestration
    - **Memory Layer** for context-aware responses
    """)

# Main content
st.markdown('<div class="main-header">💼 Bajaj AMC Fund Factsheet Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask questions about fund performance, holdings, and metrics</div>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display sources if available (sorted by similarity in descending order)
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            # Deduplicate sources using hash-based comparison
            import hashlib
            seen_content_hashes = set()
            unique_sources = []
            for source in message["sources"]:
                content_normalized = source.get("content", "").strip()
                content_hash = hashlib.md5(content_normalized.encode('utf-8')).hexdigest()
                page = source.get("metadata", {}).get('page', 'unknown')
                doc_type = source.get("metadata", {}).get('type', 'text')
                unique_key = f"{content_hash}__page_{page}__type_{doc_type}"
                
                if unique_key not in seen_content_hashes:
                    seen_content_hashes.add(unique_key)
                    unique_sources.append(source)
            
            # Sort by similarity score (descending)
            sorted_sources = sorted(unique_sources, key=lambda x: x.get("score", 0), reverse=True)
            with st.expander("📚 View Sources"):
                for idx, source in enumerate(sorted_sources, 1):
                    st.markdown(f"""
                    <div class="source-box">
                    <b>Source {idx}</b> (Similarity: {source['score']:.3f})<br>
                    {source['content']}<br>
                    <small>Page: {source['metadata'].get('page', 'N/A')} | Type: {source['metadata'].get('type', 'N/A')}</small>
                    </div>
                    """, unsafe_allow_html=True)

# Handle sample question selection
if "current_question" in st.session_state:
    user_input = st.session_state.current_question
    del st.session_state.current_question
else:
    user_input = None

# Chat input
if prompt := st.chat_input("Ask a question about the fund factsheet...") or user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching documents and generating answer..."):
            try:
                # Check if vector store exists
                vector_store = get_vector_store()

                # Run query through LangGraph workflow
                result = run_rag_query(prompt, st.session_state.chat_history)

                # Display answer
                if result.get("error"):
                    response = f"⚠️ Error: {result['error']}\n\n{result['answer']}"
                else:
                    response = result["answer"]

                # Add memory indicator
                if result.get("memory_used"):
                    response = "🧠 *Using conversation memory*\n\n" + response

                st.markdown(response)

                # Display sources (sorted by similarity in descending order - most similar first)
                if result.get("sources"):
                    # Deduplicate sources using hash-based comparison
                    import hashlib
                    seen_content_hashes = set()
                    unique_sources = []
                    for source in result["sources"]:
                        content_normalized = source.get("content", "").strip()
                        content_hash = hashlib.md5(content_normalized.encode('utf-8')).hexdigest()
                        page = source.get("metadata", {}).get('page', 'unknown')
                        doc_type = source.get("metadata", {}).get('type', 'text')
                        unique_key = f"{content_hash}__page_{page}__type_{doc_type}"
                        
                        if unique_key not in seen_content_hashes:
                            seen_content_hashes.add(unique_key)
                            unique_sources.append(source)
                    
                    # Sort by similarity score (descending)
                    sorted_sources = sorted(unique_sources, key=lambda x: x.get("score", 0), reverse=True)
                    with st.expander("📚 View Sources"):
                        for idx, source in enumerate(sorted_sources, 1):
                            st.markdown(f"""
                            <div class="source-box">
                            <b>Source {idx}</b> (Similarity: {source['score']:.3f})<br>
                            {source['content']}<br>
                            <small>Page: {source['metadata'].get('page', 'N/A')} | Type: {source['metadata'].get('type', 'N/A')}</small>
                            </div>
                            """, unsafe_allow_html=True)

                # Store assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "sources": result.get("sources", [])
                })

                # Update chat history for context
                st.session_state.chat_history.append({"user": prompt, "assistant": response})

            except Exception as e:
                error_msg = f"❌ An error occurred: {str(e)}\n\nPlease ensure:\n1. PDFs have been ingested (run `python scripts/ingest_from_folder.py`)\n2. GROQ_API_KEY is set in .env file"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": []
                })

# Footer
st.markdown("---")
st.metric("Total Messages", len(st.session_state.messages))
