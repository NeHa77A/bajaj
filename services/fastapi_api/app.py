from fastapi import FastAPI, Query
from src.fund_factsheet_rag.indexer.vector_store import similarity_search_with_relevance
from src.fund_factsheet_rag.llm.qa_generator import generate_answer

app = FastAPI(title="Fund Factsheet RAG API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/query")
def query(q: str = Query(..., description="User question")):
    """Query the RAG system and return answer with sources sorted by similarity (descending)"""
    # Get documents from FAISS (returns tuples of (Document, distance))
    # similarity_search_with_relevance already handles deduplication
    results = similarity_search_with_relevance(q, k=5)
    
    # Sort results by similarity in descending order (most similar first)
    # Convert distance to similarity for sorting: similarity = 1 / (1 + distance)
    sorted_results = sorted(
        results,
        key=lambda x: 1.0 / (1.0 + float(x[1])),  # Convert distance to similarity
        reverse=True  # Descending order (highest similarity first)
    )
    
    # Generate answer with sorted results
    result = generate_answer(q, sorted_results, source_info=True)
    
    # Ensure sources are sorted by similarity (descending) - most similar first
    # Also deduplicate sources by content using hash
    import hashlib
    sources = result.get("sources", [])
    seen_content_hashes = set()
    unique_sources = []
    for source in sources:
        content_normalized = source.get("content", "").strip()
        content_hash = hashlib.md5(content_normalized.encode('utf-8')).hexdigest()
        page = source.get("metadata", {}).get('page', 'unknown')
        doc_type = source.get("metadata", {}).get('type', 'text')
        unique_key = f"{content_hash}__page_{page}__type_{doc_type}"
        
        if unique_key not in seen_content_hashes:
            seen_content_hashes.add(unique_key)
            unique_sources.append(source)
    
    sorted_sources = sorted(unique_sources, key=lambda x: x.get("score", 0), reverse=True)
    
    return {
        "query": q,
        "answer": result["answer"],
        "sources": sorted_sources  # Sources sorted by similarity (highest first), deduplicated
    }
