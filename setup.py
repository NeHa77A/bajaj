import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.1"

# --- Project Metadata ---
REPO_NAME = "Fund-Factsheet-RAG-Chatbot"
AUTHOR_USER_NAME = "NeHa77A"
SRC_REPO = "fund_factsheet_rag"
AUTHOR_EMAIL = "nehavishwakarma7777@gmail.com"
DESCRIPTION = "A modular RAG chatbot that extracts and answers queries from fund factsheet PDFs using Hugging Face models and Chroma vector DB."

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi",
        "uvicorn",
        "streamlit",
        "pymupdf",
        "pdfplumber",
        "torch",
        "transformers",
        "sentence-transformers",
        "chromadb",
        "Pillow",
        "tqdm",
        "python-multipart",
        "PyYAML"
    ],
)
