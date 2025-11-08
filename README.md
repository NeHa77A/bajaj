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
| **Embeddings** | HuggingFace sentence-transformers | Convert text to vectors |
| **Vector Store** | FAISS | Fast similarity search for documents |
| **Memory** | FAISS (separate index) | Store & retrieve conversation history |
| **Workflow** | LangGraph | Stateful RAG pipeline orchestration |
| **LLM** | Groq (Llama 3.1 70B) | Ultra-fast answer generation |
| **UI** | Streamlit | Interactive chat interface |

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
    ├── embeddings/                # HuggingFace embeddings
    ├── indexer/                   # FAISS vector store
    ├── llm/                       # Groq LLM integration
    ├── graph/                     # LangGraph RAG workflow
    ├── memory/                    # Conversation memory layer
    └── calculations/              # Financial calculations
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Groq API Key (get one free at [console.groq.com](https://console.groq.com))

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd bajaj-main
```

### 2️⃣ Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variables
Create or update `.env` file:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5️⃣ Add PDF Factsheets
Place your Bajaj AMC factsheet PDFs in:
```bash
data/raw_pdfs/
```

### 6️⃣ Run Ingestion Pipeline
Process PDFs and build FAISS index:
```bash
python scripts/ingest_from_folder.py
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

### 7️⃣ Launch Streamlit UI
```bash
streamlit run services/streamlit_ui/app.py
```

Access at: **http://localhost:8501**

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
