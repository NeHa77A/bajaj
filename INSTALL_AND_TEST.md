# Complete Installation & Testing Guide

## Prerequisites

Before installation, you'll need API keys:

1. **Google Gemini API Key** (for embeddings)
   - Get from: https://makersuite.google.com/app/apikey
   - Free tier available
   - Lightweight - no PyTorch required!

2. **Groq API Key** (for LLM)
   - Get from: https://console.groq.com/keys
   - Free tier available

## Step-by-Step Installation

### Step 1: Install Dependencies
```bash
# Install all dependencies (no PyTorch needed!)
uv sync
```

### Step 2: Configure API Keys
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys:
# GOOGLE_API_KEY=your_google_api_key_here
# GROQ_API_KEY=your_groq_api_key_here
```

### Step 3: Verify Installation
```bash
python test_setup.py
```

### Step 4: Run the Application
```bash
# 1. Add PDFs to data/raw_pdfs/
# 2. Index documents
python scripts/ingest_from_folder.py

# 3. Launch UI
streamlit run services/streamlit_ui/app.py
```

## Expected Package Sizes
- LangChain + LangGraph: ~30MB
- HuggingFace Hub: ~20MB
- FAISS (CPU): ~17MB
- Streamlit: ~50MB
- PDF libraries: ~35MB
- **Total: ~150MB** (lightweight, no GPU/PyTorch dependencies!)

## Architecture

This application uses:
- **Google Gemini API** for embeddings (models/embedding-001) - lightweight, no PyTorch
- **Groq API** for LLM inference (Llama 3.1 70B)
- **FAISS** for vector storage (CPU-only)
- **LangChain & LangGraph** for orchestration
- **Streamlit** for UI

## Troubleshooting

### If imports fail:
```bash
# Activate virtual environment
source .venv/bin/activate

# Reinstall
uv sync
```

### If API keys not found:
```bash
# Make sure .env file exists in project root
# Verify API keys are set correctly
cat .env
```

### If embeddings fail (rate limit exceeded):
- Check GOOGLE_API_KEY is valid
- Google Gemini free tier has daily limits - wait 24 hours for reset
- Monitor usage at: https://ai.dev/usage?tab=rate-limit
- Check internet connection
