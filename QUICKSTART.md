# 🚀 Quick Start Guide
### Get the Bajaj AMC Factsheet Chatbot running in 5 minutes!

---

## Prerequisites

**For Local Development:**
✅ Python 3.11 or higher
✅ [uv](https://github.com/astral-sh/uv) - Ultrafast Python package installer
✅ Groq API Key (free at [console.groq.com](https://console.groq.com))
✅ OpenAI API Key (for embeddings - get one at [platform.openai.com](https://platform.openai.com))

**For Docker (Easier Setup):**
✅ Docker and Docker Compose
✅ Groq API Key
✅ OpenAI API Key

### Install uv (for local development)
```bash
# On Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

---

## Step-by-Step Setup

### 1. Install Dependencies
```bash
# uv automatically creates and manages the virtual environment
uv pip install -e .
# Or install from requirements.txt
uv pip install -r requirements.txt
```

### 2. Configure API Keys
Create `.env` file in the project root:
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
```

### 3. Add Your PDFs
```bash
# Place factsheet PDFs in data/raw_pdfs/
mkdir -p data/raw_pdfs
# Copy your PDF files here
```

### 4. Index the Documents
```bash
uv run python scripts/ingest_from_folder.py
```

Wait for completion (~1-2 minutes for a typical factsheet)

### 5. Launch the Chatbot

**Option A: Run with uv**
```bash
# Terminal 1: Backend
uv run uvicorn services.fastapi_api.app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
uv run streamlit run services/streamlit_ui/app.py --server.port 8501 --server.address 0.0.0.0
```

**Option B: Use Docker (Recommended)**

```bash
# Make sure you have a .env file with API keys
# Then build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Note:** Docker automatically runs PDF ingestion on startup. The backend will:
1. Process all PDFs in `data/raw_pdfs/`
2. Build the FAISS index
3. Start the FastAPI server

Open browser to: **http://localhost:8501**

---

## 🎉 You're Done!

Try asking:
- "What is the 3-year return of Bajaj Flexi Cap Fund?"
- "List the top 5 holdings with their weights"
- "Compare equity and debt allocation"

---

## 🧠 Using Memory

The chatbot remembers your conversation! Try:

1. Ask: "What's the AUM of the fund?"
2. Then ask: "How has it changed from last month?"

The second question uses context from the first!

---

## 🛠️ Troubleshooting

**Error: GROQ_API_KEY not found**
- Check your `.env` file exists
- Ensure GROQ_API_KEY is set correctly

**Error: No PDF files found**
- Add PDF files to `data/raw_pdfs/` directory
- Re-run the ingestion script

**Error: Module not found**
- Reinstall dependencies: `uv pip install -r requirements.txt`
- Or use: `uv run python <script>` to run with uv's managed environment

**Streamlit won't start**
- Check if port 8501 is available
- Try: `streamlit run services/streamlit_ui/app.py --server.port 8502`

---

## 📊 Architecture Overview

```
┌─────────────┐
│   User UI   │ ← Streamlit Chat Interface
└──────┬──────┘
       ↓
┌──────────────────┐
│  LangGraph       │ ← Workflow: Memory → Retrieve → Calculate → Generate
│  RAG Pipeline    │
└──────┬───────────┘
       ↓
┌──────────────────┬──────────────────┐
│  FAISS Index     │  Memory Index    │
│  (Documents)     │  (Conversations) │
└──────────────────┴──────────────────┘
       ↓                    ↓
┌──────────────────┬──────────────────┐
│  OpenAI          │  Groq LLM        │
│  Embeddings      │  (Llama 3.3)     │
└──────────────────┴──────────────────┘
```

---

## 🎯 Key Features

✅ **Multimodal PDF Processing** - Extracts text, tables, charts
✅ **Fast Vector Search** - FAISS for sub-second retrieval
✅ **Conversation Memory** - Context-aware follow-up questions
✅ **Financial Calculations** - CAGR, returns, ratios on-the-fly
✅ **Source Citation** - Every answer shows source documents
✅ **Groq LLM** - Lightning-fast response generation

---

## 💡 Pro Tips

1. **Clear Memory**: Click "🗑️ Clear Chat History" to reset conversation
2. **Sample Questions**: Use sidebar buttons for quick examples
3. **View Sources**: Expand "📚 View Sources" to see document references
4. **Follow-up Questions**: Ask related questions - memory makes it smarter!

---

## 📚 Learn More

- Full documentation: [README.md](README.md)
- LangChain: [python.langchain.com](https://python.langchain.com)
- LangGraph: [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)
- Groq: [console.groq.com](https://console.groq.com)

---

## 🆘 Need Help?

Check the full README for detailed documentation, architecture diagrams, and advanced configuration options.

---

**Happy Chatting! 💬**
