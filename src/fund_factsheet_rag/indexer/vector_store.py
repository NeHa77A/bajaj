"""
FAISS-based vector store implementation with LangChain
"""
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema import Document
import yaml
import os
import pickle
from pathlib import Path
from ..embeddings.text_encoder import get_embeddings

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

_vector_store = None

def get_vector_store():
    """Get or create FAISS vector store"""
    global _vector_store

    if _vector_store is None:
        index_path = CFG["paths"]["faiss_index"]
        Path(index_path).mkdir(parents=True, exist_ok=True)

        index_file = os.path.join(index_path, "index.faiss")

        embeddings = get_embeddings()

        # Load existing index or create new one
        if os.path.exists(index_file):
            _vector_store = FAISS.load_local(
                index_path,
                embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            # Create empty FAISS index
            _vector_store = FAISS.from_documents(
                [Document(page_content="initialization", metadata={})],
                embeddings
            )

    return _vector_store

def add_documents(documents: list):
    """Add documents to FAISS vector store with deduplication"""
    import hashlib
    
    vector_store = get_vector_store()
    
    # First, deduplicate within the batch itself
    # Use content hash to identify exact duplicates
    seen_content_hashes = set()
    unique_documents = []
    
    for doc in documents:
        # Normalize content: strip whitespace
        content_normalized = doc.page_content.strip()
        
        # Create hash of the full content for exact duplicate detection
        content_hash = hashlib.md5(content_normalized.encode('utf-8')).hexdigest()
        
        # Also include page and type in hash to allow same content on different pages/types
        page = doc.metadata.get('page', 'unknown')
        doc_type = doc.metadata.get('type', 'text')
        unique_key = f"{content_hash}__page_{page}__type_{doc_type}"
        
        if unique_key not in seen_content_hashes:
            seen_content_hashes.add(unique_key)
            unique_documents.append(doc)
    
    # Only add unique documents
    if unique_documents:
        vector_store.add_documents(unique_documents)
    
    return vector_store

def save_vector_store():
    """Persist FAISS index to disk"""
    vector_store = get_vector_store()
    index_path = CFG["paths"]["faiss_index"]
    vector_store.save_local(index_path)

def similarity_search(query: str, k: int = None):
    """Search for similar documents"""
    if k is None:
        k = CFG["retrieval"]["top_k"]

    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)
    return results

def similarity_search_with_relevance(query: str, k: int = None):
    """Search with relevance threshold and deduplication"""
    if k is None:
        k = CFG["retrieval"]["top_k"]

    vector_store = get_vector_store()
    threshold = CFG["retrieval"]["similarity_threshold"]

    # Get more results to filter duplicates
    results = vector_store.similarity_search_with_score(query, k=k * 2)

    # Filter by threshold (lower score = more similar for FAISS)
    filtered_results = [(doc, score) for doc, score in results if score >= threshold]

    # Deduplicate based on document content (use hash for exact duplicates)
    import hashlib
    seen_content_hashes = set()
    unique_results = []
    for doc, score in filtered_results:
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
            if len(unique_results) >= k:
                break

    return unique_results
