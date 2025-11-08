"""
Test script to verify complete installation and functionality
Run this after installation to ensure everything works
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test all critical imports"""
    print("\n" + "="*60)
    print("Testing Package Imports")
    print("="*60)

    tests = {
        "LangChain": ["langchain", "langchain_community", "langchain_groq", "langchain_google_genai"],
        "LangGraph": ["langgraph"],
        "Vector Store": ["faiss"],
        "LLM": ["groq"],
        "Embeddings": ["google.generativeai"],
        "PDF Processing": ["fitz", "pdfplumber"],
        "UI": ["streamlit"],
        "Utilities": ["yaml", "dotenv", "numpy", "tqdm"]
    }

    failed = []

    for category, packages in tests.items():
        print(f"\n{category}:")
        for pkg in packages:
            try:
                __import__(pkg)
                print(f"  ✅ {pkg}")
            except ImportError as e:
                print(f"  ❌ {pkg} - {e}")
                failed.append(pkg)

    if failed:
        print(f"\n⚠️  Failed imports: {', '.join(failed)}")
        return False

    print("\n✅ All imports successful!")
    return True

def test_google_api():
    """Test Google Gemini API configuration"""
    print("\n" + "="*60)
    print("Testing Google Gemini API")
    print("="*60)

    from dotenv import load_dotenv
    load_dotenv()

    google_key = os.getenv("GOOGLE_API_KEY")

    if google_key:
        print(f"  ✅ GOOGLE_API_KEY found: {google_key[:10]}...")
        return True
    else:
        print("  ❌ GOOGLE_API_KEY not found in .env file")
        print("     Create .env file with: GOOGLE_API_KEY=your_key_here")
        print("     Get key from: https://makersuite.google.com/app/apikey")
        return False

def test_environment():
    """Test environment configuration"""
    print("\n" + "="*60)
    print("Testing Environment Configuration")
    print("="*60)

    from dotenv import load_dotenv
    load_dotenv()

    groq_key = os.getenv("GROQ_API_KEY")

    if groq_key:
        print(f"  ✅ GROQ_API_KEY found: {groq_key[:10]}...")
    else:
        print("  ❌ GROQ_API_KEY not found in .env file")
        print("     Create .env file with: GROQ_API_KEY=your_key_here")
        return False

    return True

def test_directories():
    """Test directory structure"""
    print("\n" + "="*60)
    print("Testing Directory Structure")
    print("="*60)

    required_dirs = [
        "configs",
        "data/raw_pdfs",
        "src/fund_factsheet_rag",
        "services/streamlit_ui",
        "scripts"
    ]

    for dir_path in required_dirs:
        full_path = Path(dir_path)
        if full_path.exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - missing")

    return True

def test_config():
    """Test configuration file"""
    print("\n" + "="*60)
    print("Testing Configuration File")
    print("="*60)

    try:
        import yaml

        config_path = "configs/config.yaml"
        if not Path(config_path).exists():
            print(f"  ❌ {config_path} not found")
            return False

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        required_keys = ["models", "paths", "vector_db", "memory", "retrieval"]

        for key in required_keys:
            if key in config:
                print(f"  ✅ {key}: {list(config[key].keys())}")
            else:
                print(f"  ❌ {key} - missing")

        return True
    except Exception as e:
        print(f"  ❌ Config test failed: {e}")
        return False

def test_embeddings():
    """Test embeddings functionality"""
    print("\n" + "="*60)
    print("Testing Embeddings")
    print("="*60)

    try:
        from src.fund_factsheet_rag.embeddings.text_encoder import get_embeddings, embed_query

        embeddings = get_embeddings()
        print(f"  ✅ Embeddings model loaded")

        test_text = "What is the 3-year return of Bajaj Flexi Cap Fund?"
        embedding = embed_query(test_text)

        print(f"  ✅ Test embedding generated")
        print(f"     Dimension: {len(embedding)}")
        print(f"     Sample values: {embedding[:3]}")

        return True
    except Exception as e:
        print(f"  ❌ Embeddings test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_groq_connection():
    """Test Groq API connection"""
    print("\n" + "="*60)
    print("Testing Groq API Connection")
    print("="*60)

    try:
        from src.fund_factsheet_rag.llm.qa_generator import get_llm
        from langchain.schema import HumanMessage

        llm = get_llm()
        print(f"  ✅ Groq LLM initialized")

        # Simple test query
        response = llm.invoke([HumanMessage(content="Say 'Hello' in one word")])
        print(f"  ✅ API call successful")
        print(f"     Response: {response.content}")

        return True
    except Exception as e:
        print(f"  ❌ Groq test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_processing():
    """Test PDF processing (if PDFs exist)"""
    print("\n" + "="*60)
    print("Testing PDF Processing")
    print("="*60)

    pdf_dir = Path("data/raw_pdfs")
    pdfs = list(pdf_dir.glob("*.pdf"))

    if not pdfs:
        print("  ⚠️  No PDFs found in data/raw_pdfs/")
        print("     Add PDF files to test ingestion")
        return True

    print(f"  ✅ Found {len(pdfs)} PDF(s)")

    try:
        from src.fund_factsheet_rag.ingestion.pdf_reader import process_pdf_to_documents, chunk_documents

        # Test on first PDF
        test_pdf = pdfs[0]
        print(f"     Testing with: {test_pdf.name}")

        documents = process_pdf_to_documents(str(test_pdf))
        print(f"  ✅ Extracted {len(documents)} documents")

        chunks = chunk_documents(documents[:5])  # Test with first 5 docs
        print(f"  ✅ Created {len(chunks)} chunks")

        return True
    except Exception as e:
        print(f"  ❌ PDF processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vector_store():
    """Test FAISS vector store"""
    print("\n" + "="*60)
    print("Testing FAISS Vector Store")
    print("="*60)

    try:
        from src.fund_factsheet_rag.indexer.vector_store import get_vector_store

        vector_store = get_vector_store()
        print(f"  ✅ FAISS vector store initialized")

        return True
    except Exception as e:
        print(f"  ❌ Vector store test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory():
    """Test conversation memory"""
    print("\n" + "="*60)
    print("Testing Conversation Memory")
    print("="*60)

    try:
        from src.fund_factsheet_rag.memory.conversation_memory import get_memory_manager

        memory = get_memory_manager()
        print(f"  ✅ Memory manager initialized")

        # Test adding a conversation
        memory.add_conversation_turn(
            user_message="Test question",
            assistant_message="Test answer",
            metadata={"test": True}
        )
        print(f"  ✅ Conversation added to memory")

        # Test retrieval
        recent = memory.get_recent_history(n=1)
        print(f"  ✅ Retrieved {len(recent)} recent conversation(s)")

        return True
    except Exception as e:
        print(f"  ❌ Memory test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_langgraph_workflow():
    """Test LangGraph workflow"""
    print("\n" + "="*60)
    print("Testing LangGraph RAG Workflow")
    print("="*60)

    try:
        from src.fund_factsheet_rag.graph.rag_workflow import create_rag_workflow

        workflow = create_rag_workflow()
        print(f"  ✅ LangGraph workflow created")
        print(f"     Nodes: {list(workflow.nodes.keys()) if hasattr(workflow, 'nodes') else 'N/A'}")

        return True
    except Exception as e:
        print(f"  ❌ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 BAJAJ AMC FACTSHEET RAG - SYSTEM TEST")
    print("="*60)

    tests = [
        ("Package Imports", test_imports),
        ("Google Gemini API", test_google_api),
        ("Environment Variables", test_environment),
        ("Directory Structure", test_directories),
        ("Configuration File", test_config),
        ("Embeddings", test_embeddings),
        ("Groq API", test_groq_connection),
        ("PDF Processing", test_pdf_processing),
        ("FAISS Vector Store", test_vector_store),
        ("Conversation Memory", test_memory),
        ("LangGraph Workflow", test_langgraph_workflow),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results[test_name] = False

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Add PDF files to data/raw_pdfs/")
        print("2. Run: python scripts/ingest_from_folder.py")
        print("3. Run: streamlit run services/streamlit_ui/app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")

    print("="*60)

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
