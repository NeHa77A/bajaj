# 💼 Bajaj AMC Fund Factsheet RAG Chatbot
### _Intelligent Multimodal RAG System using LangChain, LangGraph, FAISS & Groq_

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Store-orange)
![Groq](https://img.shields.io/badge/Groq-LLM-purple)

---

## 📘 Overview

The **Bajaj AMC Fund Factsheet RAG Chatbot** is a production-ready **Retrieval-Augmented Generation (RAG)** system that:
- Extracts **text, tables, and charts** from fund factsheet PDFs
- Uses **LangChain** for document processing and embeddings
- Implements **LangGraph** for stateful RAG workflow orchestration
- Stores embeddings in **FAISS** vector database
- Uses **Groq API** for ultra-fast LLM inference
- Provides an interactive **Streamlit** chat interface

Built specifically for the Bajaj AMC Fund Factsheet challenge, supporting complex queries about fund performance, holdings, risk metrics, and calculations.

---

## 🎥 Demo Video

Watch the application in action:

<video width="800" controls>
  <source src="video1.webm" type="video/webm">
  Your browser does not support the video tag.
</video>

---

## 🧩 Key Features

✅ **Multimodal PDF Processing**: Extracts text, tables, and images from PDFs

✅ **LangChain Integration**: Document loaders, text splitting, and embeddings

✅ **LangGraph Workflow**: Stateful RAG pipeline with retrieval → calculation → generation

✅ **FAISS Vector Store**: Fast, efficient similarity search

✅ **Groq LLM**: Lightning-fast inference with Llama 3.1 70B

✅ **Financial Calculations**: CAGR, returns, ratios computed on-the-fly

✅ **Source Attribution**: Every answer cites relevant document sections

✅ **Interactive UI**: Modern Streamlit chat interface with sample questions

✅ **Context-Aware**: Maintains conversation history for follow-up questions

---

## 🏗️ Architecture

### LangGraph RAG Workflow

https://whimsical.com/JjEL3zCJVhZFhh274sVLND


![Architecture](https://raw.githubusercontent.com/NeHa77A/bajaj/refs/heads/dev/bajaj_hld.png)

```
User Query
    ↓
┌─────────────────┐
│  Load Memory    │ ← Retrieves relevant conversation history from FAISS
└────────┬────────┘
         ↓
┌─────────────────┐
│  Retrieve Docs  │ ← Searches factsheet content in FAISS
└────────┬────────┘
         ↓
┌─────────────────┐
│ Check Calc Need │ ← Determines if financial calculation needed
└────────┬────────┘
         ↓
┌─────────────────┐
│  Calculate      │ ← Performs CAGR, returns, ratios (if needed)
└────────┬────────┘
         ↓
┌─────────────────┐
│ Generate Answer │ ← Uses Groq LLM to create response
│  + Save Memory  │    Saves conversation to memory
└────────┬────────┘
         ↓
    Response with Sources
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Document Loading** | LangChain PyMuPDFLoader | Extract text, tables, images from PDFs |
| **Text Splitting** | RecursiveCharacterTextSplitter | Chunk documents for embedding |
| **Embeddings** | OpenAI text-embedding-3-small | Convert text to vectors |
| **Vector Store** | FAISS | Fast similarity search for documents |
| **Memory** | FAISS (separate index) | Store & retrieve conversation history |
| **Workflow** | LangGraph | Stateful RAG pipeline orchestration |
| **LLM** | Groq (Llama 3.3 70B) | Ultra-fast answer generation |
| **Backend** | FastAPI | REST API for query endpoints |
| **UI** | Streamlit | Interactive chat interface |
| **Package Manager** | uv | Fast Python package installer and runner |

## 📁 Project Structure

```
bajaj-main/
├── .env                           # Environment variables (GROQ_API_KEY)
├── configs/
│   └── config.yaml                # Global configuration
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
│
├── data/
│   ├── raw_pdfs/                  # Input fund factsheets
│   ├── extracted_images/          # Extracted charts/images
│   ├── faiss_index/              # FAISS vector store
│   └── memory_index/             # Conversation memory store
│
├── scripts/
│   └── ingest_from_folder.py      # PDF ingestion script
│
├── services/
│   └── streamlit_ui/
│       └── app.py                 # Streamlit UI
│
└── src/fund_factsheet_rag/
    ├── ingestion/                 # PDF processing (LangChain loaders)
    ├── embeddings/                # OpenAI embeddings
    ├── indexer/                   # FAISS vector store
    ├── llm/                       # Groq LLM integration
    ├── graph/                     # LangGraph RAG workflow
    ├── memory/                    # Conversation memory layer
    └── calculations/              # Financial calculations
```

---

## ⚙️ Installation & Setup

### Prerequisites

**Option 1: Local Development (with uv)**
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Ultrafast Python package installer and resolver
- Groq API Key (get one free at [console.groq.com](https://console.groq.com))
- OpenAI API Key (for embeddings - get one at [platform.openai.com](https://platform.openai.com))

**Option 2: Docker (Recommended for Production)**
- Docker and Docker Compose installed
- Groq API Key
- OpenAI API Key

### Install uv
```bash
# On Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd bajaj-main
```

### 2️⃣ Choose Your Setup Method

**Quick Start with Docker (Recommended):**
```bash
# 1. Create .env file with your API keys
echo "GROQ_API_KEY=your_key" > .env
echo "OPENAI_API_KEY=your_key" >> .env

# 2. Add PDFs to data/raw_pdfs/
# (Place your factsheet PDFs here)

# 3. Start everything with Docker
docker-compose up --build

# That's it! Docker will:
# - Install all dependencies
# - Process PDFs and build FAISS index
# - Start backend and frontend
# Access at http://localhost:8501
```

**Or Continue with Local Setup:**

### 2️⃣ Install Dependencies with uv
```bash
# uv automatically creates and manages the virtual environment
uv pip install -e .
# Or install from requirements.txt
uv pip install -r requirements.txt
```

### 3️⃣ Set Environment Variables
Create or update `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 4️⃣ Add PDF Factsheets
Place your Bajaj AMC factsheet PDFs in:
```bash
data/raw_pdfs/
```

### 5️⃣ Run Ingestion Pipeline
Process PDFs and build FAISS index:
```bash
uv run python scripts/ingest_from_folder.py
```

Expected output:
```
============================================================
Fund Factsheet RAG - Document Ingestion
Using: LangChain + FAISS + Groq
============================================================

📚 Found 1 PDF file(s) to process

📄 Processing: Bajaj_Factsheet_Oct2025.pdf
  ├─ Extracting content...
  ├─ Extracted 15 document sections
  ├─ Chunking documents...
  ├─ Created 45 chunks
  ├─ Adding to FAISS index...
  ✓ Successfully indexed Bajaj_Factsheet_Oct2025.pdf

💾 Saving FAISS index to disk...

============================================================
✅ Ingestion Complete!
   Total PDFs processed: 1
   Total chunks indexed: 45
   Index saved to: data/faiss_index
============================================================
```

### 6️⃣ Launch Services

**Option A: Run Backend and Frontend Separately**

```bash
# Terminal 1: Start FastAPI Backend
uv run uvicorn services.fastapi_api.app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Streamlit Frontend
uv run streamlit run services/streamlit_ui/app.py --server.port 8501 --server.address 0.0.0.0
```

**Option B: Use Docker Compose (Recommended for Production)**

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Docker Setup Details:**
- **Backend Service**: Automatically runs PDF ingestion on startup, then starts FastAPI server
- **Frontend Service**: Starts Streamlit UI (waits for backend to be ready)
- **Volumes**: 
  - `./data` - PDFs and extracted images (persisted)
  - `./artifacts` - FAISS vector store (persisted)
- **Environment**: Loads variables from `.env` file
- **Ports**: 
  - Backend: `8000` (FastAPI)
  - Frontend: `8501` (Streamlit)

**Access:**
- Streamlit UI: **http://localhost:8501**
- FastAPI Docs: **http://localhost:8000/docs**
- Health Check: **http://localhost:8000/health**

---

## 🎯 Example Questions

Try these questions with the chatbot:

1. "What is the 3-year return of Bajaj Flexi Cap Fund?"
2. "List top 5 holdings of the Consumption Fund with weights"
3. "Compare the allocation between equity and debt"
4. "How has AUM changed compared to last month?"
5. "Which equity fund has the highest 3-year return?"
6. "State the YTM and Macaulay Duration for the Money Market Fund"

---

## 🧠 Memory & Context Awareness

The chatbot maintains conversation memory using a separate FAISS index:
- **Recent History**: Last 3-5 conversation turns
- **Semantic Retrieval**: Relevant past conversations based on similarity
- **Context Integration**: Uses memory to answer follow-up questions

Example:
```
User: "What's the top holding of Flexi Cap Fund?"
Bot: "The top holding is XYZ Ltd at 8.5%"

User: "What about the second one?"  ← Context-aware!
Bot: 🧠 Using conversation memory
     "The second holding is ABC Corp at 7.2%"
```

---

## 🛠️ Troubleshooting

### Docker Issues

**Ports already in use:**
```bash
# Stop existing containers
docker-compose down

# Or change ports in docker-compose.yml
```

**Docker build fails:**
```bash
# Clean build (no cache)
docker-compose build --no-cache

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

**Environment variables not loading:**
- Ensure `.env` file exists in project root
- Check file has correct format: `KEY=value` (no spaces around `=`)
- Restart containers: `docker-compose restart`

**FAISS index not persisting:**
- Check volume mount: `./artifacts:/app/artifacts` in docker-compose.yml
- Ensure `artifacts/` directory exists locally
- Check permissions: `chmod -R 755 artifacts/`

### Local Development Issues

**Module not found errors:**
```bash
# Reinstall with uv
uv pip install -r requirements.txt

# Or use uv run for all commands
uv run python scripts/ingest_from_folder.py
```

**API Key errors:**
- Verify `.env` file exists and contains both `GROQ_API_KEY` and `OPENAI_API_KEY`
- Check no extra spaces or quotes in `.env` file
- Restart services after updating `.env`

**Port conflicts:**
```bash
# Kill processes on ports 8000/8501
fuser -k 8000/tcp 8501/tcp

# Or use different ports
uv run uvicorn services.fastapi_api.app:app --port 8001
uv run streamlit run services/streamlit_ui/app.py --server.port 8502
```

**PDF ingestion fails:**
- Ensure PDFs are in `data/raw_pdfs/` directory
- Check PDF files are not corrupted
- Verify sufficient disk space for FAISS index

---
