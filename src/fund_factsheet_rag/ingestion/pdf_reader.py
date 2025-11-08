"""
PDF processing module using LangChain document loaders
Enhanced with Groq vision for image/table processing
"""
from langchain_community.document_loaders import PyMuPDFLoader, PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import fitz
import pdfplumber
from pathlib import Path
from PIL import Image
import yaml
import os
from ..extraction.vision_processor import describe_image_with_groq, describe_table_with_groq

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

def load_pdf_with_langchain(pdf_path: str):
    """
    Load PDF using LangChain PyMuPDF loader
    """
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    return documents

def extract_pages_and_images(pdf_path: str, out_dir: str = None):
    """
    Extract text and images from PDF using PyMuPDF
    Returns structured data for processing
    Fixed colorspace handling for PNG export
    """
    if out_dir is None:
        out_dir = CFG["paths"]["extracted_images"]

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    pages_data = []

    for i, page in enumerate(doc):
        text = page.get_text("text")
        images = []

        # Extract images with proper colorspace handling
        for idx, img in enumerate(page.get_images(full=True)):
            try:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # Save directly from bytes to avoid colorspace issues
                img_path = f"{out_dir}/page{i+1}_img{idx}.png"
                with open(img_path, "wb") as img_file:
                    img_file.write(image_bytes)

                images.append(img_path)
            except Exception as e:
                print(f"  ⚠️  Failed to extract image {idx} from page {i+1}: {e}")
                continue

        pages_data.append({
            "page": i + 1,
            "text": text,
            "images": images
        })

    return pages_data

def extract_tables_from_pdf(pdf_path: str):
    """
    Extract tables from PDF using pdfplumber
    """
    tables_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()

            for table_idx, table in enumerate(tables):
                if table:
                    # Convert table to text format
                    table_text = "\n".join([" | ".join([str(cell) if cell else "" for cell in row]) for row in table])

                    tables_data.append({
                        "page": page_num + 1,
                        "table_index": table_idx,
                        "content": table_text,
                        "raw_data": table
                    })

    return tables_data

def process_pdf_to_documents(pdf_path: str, use_vision: bool = True) -> list:
    """
    Process PDF and return LangChain Document objects
    Combines text, tables, and image descriptions using Groq vision

    Args:
        pdf_path: Path to PDF file
        use_vision: If True, use Groq vision to describe images/tables
    """
    documents = []

    print("  ├─ Extracting text content...")
    # 1. Load basic text content
    base_docs = load_pdf_with_langchain(pdf_path)

    print("  ├─ Extracting images...")
    # 2. Extract detailed page data with images
    pages_data = extract_pages_and_images(pdf_path)

    print("  ├─ Extracting tables...")
    # 3. Extract tables
    tables_data = extract_tables_from_pdf(pdf_path)

    # Create documents from pages
    for idx, doc in enumerate(base_docs):
        page_num = idx + 1
        metadata = {
            "source": pdf_path,
            "page": page_num,
            "type": "text"
        }

        documents.append(Document(
            page_content=doc.page_content,
            metadata=metadata
        ))

    # Create documents from images using Groq vision
    if use_vision:
        print("  ├─ Processing images with Groq vision...")
        for page_data in pages_data:
            for img_path in page_data["images"]:
                print(f"    • Analyzing image: {os.path.basename(img_path)}")
                description = describe_image_with_groq(img_path)

                metadata = {
                    "source": pdf_path,
                    "page": page_data["page"],
                    "type": "image",
                    "image_path": img_path
                }

                documents.append(Document(
                    page_content=f"Image from page {page_data['page']}:\n{description}",
                    metadata=metadata
                ))

    # Create documents from tables using Groq
    if use_vision:
        print("  ├─ Processing tables with Groq...")
        for table in tables_data:
            print(f"    • Analyzing table from page {table['page']}")
            description = describe_table_with_groq(table['content'])

            metadata = {
                "source": pdf_path,
                "page": table["page"],
                "type": "table",
                "table_index": table["table_index"]
            }

            # Store both original table and description
            content = f"Table from page {table['page']}:\n\nOriginal Data:\n{table['content']}\n\nAnalysis:\n{description}"

            documents.append(Document(
                page_content=content,
                metadata=metadata
            ))

    return documents

def chunk_documents(documents: list, chunk_size: int = None, chunk_overlap: int = None):
    """
    Split documents into chunks using LangChain text splitter
    """
    if chunk_size is None:
        chunk_size = CFG["langchain"]["chunk_size"]
    if chunk_overlap is None:
        chunk_overlap = CFG["langchain"]["chunk_overlap"]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunked_docs = text_splitter.split_documents(documents)
    return chunked_docs
