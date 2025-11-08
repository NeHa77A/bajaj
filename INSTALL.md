# Installation Guide - Optimized for CPU Only

## ⚠️ Important: Avoid Heavy GPU Dependencies

This project uses **sentence-transformers** for embeddings, which requires PyTorch. By default, PyTorch may try to install CUDA/GPU versions (850MB+ of NVIDIA packages).

## 🎯 Recommended Installation (CPU-only PyTorch)

### Option 1: Using `uv` (Recommended)

```bash
# 1. Install PyTorch CPU-only FIRST
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 2. Then sync the rest
uv sync

# 3. Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
# Should show: PyTorch: 2.x.x, CUDA: False
```

### Option 2: Using regular `pip`

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install PyTorch CPU-only
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 3. Install other dependencies
pip install -e .
```

### Option 3: Lightweight Alternative (No PyTorch)

If you want to completely avoid PyTorch, use this alternative approach:

```bash
# Use OpenAI embeddings instead of sentence-transformers
uv pip install langchain-openai

# Then modify the code to use OpenAI embeddings
# (requires OPENAI_API_KEY in .env)
```

## 📦 Dependency Breakdown

| Package | Size | Why Needed | Can Remove? |
|---------|------|------------|-------------|
| `torch` | ~200MB (CPU) / ~850MB (GPU) | Required by sentence-transformers | ⚠️ No (unless using alternative) |
| `sentence-transformers` | ~50MB | For embeddings | ⚠️ No (core feature) |
| `faiss-cpu` | ~17MB | Vector database | ❌ No |
| `langchain` + `langgraph` | ~30MB | RAG framework | ❌ No |
| `groq` | ~5MB | LLM inference | ❌ No |
| `streamlit` | ~50MB | UI | ❌ No |
| `pymupdf` + `pdfplumber` | ~35MB | PDF processing | ❌ No |
| **TOTAL (CPU)** | **~400MB** | | |
| **TOTAL (with GPU)** | **~1.2GB+** | | |

## 🚫 What We DON'T Need

- ❌ `nvidia-nccl-cu12` (307MB) - GPU communication
- ❌ `nvidia-nvshmem-cu12` (118MB) - GPU memory management
- ❌ `triton` (162MB) - GPU compiler
- ❌ Any CUDA packages - We only use CPU

## ✅ Final Installation Steps

```bash
# 1. Install CPU-only PyTorch
uv pip install torch --index-url https://download.pytorch.org/whl/cpu

# 2. Sync dependencies
uv sync

# 3. Set up environment
echo "GROQ_API_KEY=your_key_here" > .env

# 4. Verify installation
python -c "import torch; import sentence_transformers; import faiss; print('✅ All dependencies OK')"
```

## 🔧 Troubleshooting

**Still downloading CUDA packages?**
```bash
# Force reinstall PyTorch CPU
uv pip uninstall torch torchvision
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu --force-reinstall
```

**Out of disk space?**
```bash
# Clean pip cache
uv cache clean
```

**Alternative: Use Groq Embeddings API (Coming Soon)**
```bash
# Groq may release embeddings API in the future
# This would eliminate the need for sentence-transformers entirely
```

---

## 🎯 Quick Start After Installation

```bash
# 1. Add PDFs
mkdir -p data/raw_pdfs
# Copy your factsheet PDFs here

# 2. Index documents
python scripts/ingest_from_folder.py

# 3. Launch chatbot
streamlit run services/streamlit_ui/app.py
```

---

**Need help?** Check the main [README.md](README.md) or [QUICKSTART.md](QUICKSTART.md)
