"""
Embedding module using OpenAI API
Lightweight solution - no PyTorch required, excellent rate limits
"""
from langchain_openai import OpenAIEmbeddings
import os
import yaml
from dotenv import load_dotenv

load_dotenv()

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

_embeddings = None

def get_embeddings():
    """
    Get or create OpenAI embeddings instance
    Uses OpenAI's API - requires OPENAI_API_KEY
    Lightweight solution with no PyTorch dependencies and excellent rate limits
    """
    global _embeddings
    if _embeddings is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        model_name = CFG["models"]["text_embedding"]

        # Use OpenAI Embeddings
        _embeddings = OpenAIEmbeddings(
            model=model_name,
            openai_api_key=api_key
        )
    return _embeddings

def embed_documents(texts: list) -> list:
    """Embed a list of documents"""
    embeddings = get_embeddings()
    return embeddings.embed_documents(texts)

def embed_query(text: str) -> list:
    """Embed a single query"""
    embeddings = get_embeddings()
    return embeddings.embed_query(text)

def encode_texts(texts: list) -> list:
    """Embed a list of texts (alias for embed_documents for compatibility)"""
    return embed_documents(texts)
