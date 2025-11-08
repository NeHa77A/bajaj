import yaml
from src.fund_factsheet_rag.indexer.vector_store import similarity_search_with_relevance

CFG = yaml.safe_load(open("configs/config.yaml"))

def retrieve(query: str, top_k: int = None):
    """Retrieve relevant documents using FAISS vector store"""
    top_k = top_k or CFG["retrieval"]["top_k"]
    
    # Use FAISS similarity search
    results = similarity_search_with_relevance(query, k=top_k)
    
    hits = []
    for doc, distance in results:
        # Convert FAISS distance to similarity score (higher = more similar)
        # FAISS returns L2 distance where lower = more similar
        # Convert to similarity: similarity = 1 / (1 + distance)
        # This ensures higher similarity scores for more similar documents
        similarity = 1.0 / (1.0 + float(distance))
        
        hits.append({
            "document": doc.page_content,
            "metadata": doc.metadata,
            "score": similarity
        })
    
    # Sort by similarity score in descending order (most similar first)
    hits.sort(key=lambda x: x["score"], reverse=True)
    
    return hits
