import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s ")

# Project package name
package_name = "fund_factsheet_rag"

# List of files and folders to create
list_of_files = [
    # --- Core directories ---
    "data/raw_pdfs/.gitkeep",
    "data/extracted_images/.gitkeep",
    "data/parsed_tables/.gitkeep",
    "scripts/__init__.py",
    "tests/unit/__init__.py",
    "tests/integration/__init__.py",

    # --- Source core modules ---
    f"src/{package_name}/__init__.py",
    f"src/{package_name}/ingestion/__init__.py",
    f"src/{package_name}/extraction/__init__.py",
    f"src/{package_name}/preprocessing/__init__.py",
    f"src/{package_name}/embeddings/__init__.py",
    f"src/{package_name}/indexer/__init__.py",
    f"src/{package_name}/retriever/__init__.py",
    f"src/{package_name}/calculations/__init__.py",
    f"src/{package_name}/storage/__init__.py",

    # --- Individual Python files ---
    f"src/{package_name}/ingestion/pdf_reader.py",
    f"src/{package_name}/extraction/table_extractor.py",
    f"src/{package_name}/extraction/ocr.py",
    f"src/{package_name}/preprocessing/captioner.py",
    f"src/{package_name}/embeddings/text_encoder.py",
    f"src/{package_name}/indexer/vector_store.py",
    f"src/{package_name}/retriever/retriever.py",
    f"src/{package_name}/calculations/finance.py",

    # --- Service layer (APIs and UI) ---
    "services/fastapi_api/app.py",
    "services/fastapi_api/routes/__init__.py",
    "services/fastapi_api/routes/query_routes.py",
    "services/streamlit_ui/app.py",
    "services/streamlit_ui/__init__.py",

    # --- Scripts ---
    "scripts/ingest_from_folder.py",

    # --- Configs & requirements ---
    "configs/config.yaml",
    "requirements.txt",
    "README.md",
    ".env",
    "setup.py",
]

# Create all directories and files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Create folder if it doesn't exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir} for file: {filename}")

    # Create empty file if not exists
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Created empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")

logging.info("✅ Project template successfully created!")
