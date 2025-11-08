"""
Vision processing module using Groq's multimodal model via LangChain
Processes images and tables from PDFs to generate text descriptions
"""
import os
import base64
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import yaml

load_dotenv()

# Load config
with open("configs/config.yaml", "r") as f:
    CFG = yaml.safe_load(f)

def encode_image_to_base64(image_path: str) -> str:
    """
    Encode image to base64 string for API
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def describe_image_with_groq(image_path: str, prompt: str = None) -> str:
    """
    Use Groq's vision model via LangChain to describe an image
    Args:
        image_path: Path to the image file
        prompt: Custom prompt for the vision model
    Returns:
        Text description of the image
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    if prompt is None:
        prompt = """Analyze this image from a financial fund factsheet.
Describe what you see including:
- Any charts, graphs, or tables
- Key metrics and numbers
- Important labels and headings
- Overall structure and layout

Be precise and detailed, focusing on the financial data presented."""

    try:
        # Encode image
        base64_image = encode_image_to_base64(image_path)

        # Initialize LangChain ChatGroq
        llm = ChatGroq(
            model="llama-3.2-90b-vision-preview",
            groq_api_key=api_key,
            temperature=0.2,
            max_tokens=1024
        )

        # Create message with image
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        )

        # Get response
        response = llm.invoke([message])
        return response.content

    except Exception as e:
        print(f"  ⚠️  Error processing image with Groq vision: {e}")
        return f"[Image could not be processed: {str(e)}]"

def describe_table_with_groq(table_text: str) -> str:
    """
    Use Groq via LangChain to generate a natural language description of a table
    Args:
        table_text: Raw table data as text
    Returns:
        Natural language description of the table
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    prompt = f"""Analyze this table from a financial fund factsheet and provide a clear, natural language summary:

{table_text}

Focus on:
- Key metrics and their values
- Trends or patterns
- Important financial data
- Context that would help answer queries about this fund

Be concise but informative."""

    try:
        # Initialize LangChain ChatGroq
        llm = ChatGroq(
            model=CFG["models"]["groq_model"],
            groq_api_key=api_key,
            temperature=0.3,
            max_tokens=512
        )

        # Get response
        response = llm.invoke([
            HumanMessage(content="You are a financial analyst expert at interpreting fund data."),
            HumanMessage(content=prompt)
        ])

        return response.content

    except Exception as e:
        print(f"  ⚠️  Error processing table with Groq: {e}")
        return table_text  # Return original if processing fails
