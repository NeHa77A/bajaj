"""
Ingestion script for processing PDFs and building FAISS index
Using LangChain, FAISS, and the refactored modules
"""
import os
import sys
import yaml
from pathlib import Path
from tqdm import tqdm

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
from src.fund_factsheet_rag.ingestion.pdf_reader import (
    process_pdf_to_documents,
    chunk_documents
)
from src.fund_factsheet_rag.indexer.vector_store import (
    add_documents,
    save_vector_store
)

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

PDF_DIR = CFG["paths"]["raw_pdfs"]

def ingest_pdf(pdf_path: str) -> int:
    """
    Process a single PDF and add to FAISS vector store

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Number of chunks added to the index
    """
    pdf_name = os.path.basename(pdf_path)
    print(f"\n📄 Processing: {pdf_name}")

    try:
        # Step 1: Extract documents from PDF (text, tables)
        # Note: Vision processing disabled temporarily due to library version conflict
        print("  ├─ Extracting content...")
        documents = process_pdf_to_documents(pdf_path, use_vision=False)
        print(f"  ├─ Extracted {len(documents)} document sections")

        # Step 2: Chunk documents
        print("  ├─ Chunking documents...")
        chunked_docs = chunk_documents(documents)
        print(f"  ├─ Created {len(chunked_docs)} chunks")

        # Step 3: Add to FAISS vector store
        print("  ├─ Adding to FAISS index...")
        add_documents(chunked_docs)
        print(f"  ✓ Successfully indexed {pdf_name}")

        return len(chunked_docs)

    except Exception as e:
        print(f"  ✗ Error processing {pdf_name}: {str(e)}")
        return 0

def main():
    """
    Main ingestion function
    Processes all PDFs in the raw_pdfs directory
    """
    print("=" * 60)
    print("Fund Factsheet RAG - Document Ingestion")
    print("Using: LangChain + FAISS + Groq")
    print("=" * 60)

    # Ensure directories exist
    Path(PDF_DIR).mkdir(parents=True, exist_ok=True)
    Path(CFG["paths"]["faiss_index"]).mkdir(parents=True, exist_ok=True)
    Path(CFG["paths"]["extracted_images"]).mkdir(parents=True, exist_ok=True)

    # Get all PDFs
    pdfs = list(Path(PDF_DIR).glob("*.pdf"))

    if not pdfs:
        print(f"\n⚠️  No PDF files found in {PDF_DIR}")
        print("Please add PDF files to the directory and run again.")
        return

    print(f"\n📚 Found {len(pdfs)} PDF file(s) to process\n")

    total_chunks = 0

    # Process each PDF
    for pdf_path in tqdm(pdfs, desc="Processing PDFs"):
        chunks_added = ingest_pdf(str(pdf_path))
        total_chunks += chunks_added

    # Save the FAISS index
    print("\n💾 Saving FAISS index to disk...")
    save_vector_store()

    print("\n" + "=" * 60)
    print(f"✅ Ingestion Complete!")
    print(f"   Total PDFs processed: {len(pdfs)}")
    print(f"   Total chunks indexed: {total_chunks}")
    print(f"   Index saved to: {CFG['paths']['faiss_index']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
