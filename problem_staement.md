The Bajaj AMC Factsheet Chatbot

Background
Bajaj Finserv Asset Management Company (AMC) releases monthly fund factsheets that include details like portfolio holdings, asset allocation, returns, risk ratios, and fund manager commentary.These factsheets have a mix of text, tables, charts, and images, which contain valuable insights for investors and analysts.
As these reports become more detailed, it’s difficult to manually find or compare information. That’s where AI chatbots can help - by reading and understanding these documents and answering user questions naturally and accurately.

Your Challenge
Build an AI chatbot using the Retrieval-Augmented Generation (RAG) approach that can read and answer questions from the Bajaj AMC Fund Factsheet (Oct 2025). The chatbot must only use the information present in the factsheet - no outside data.

What Your Chatbot Should Do
    1. Read the provided Fund Factsheet PDF (which includes text, tables, charts, and images).
    2. Extract and store all useful information (text, numbers, data from tables or charts).
    3. Answer user questions accurately using only the data from the document.
    4. Perform simple to complex calculations, such as:
        ◦ Calculate CAGR or average returns
        ◦ Compare fund performance over different time periods
        ◦ Analyse asset allocation (e.g., debt vs. equity)
        ◦ Explain risk metrics like the Sharpe ratio

Example Questions
    • “What is the 3-year return of Bajaj Flexi Cap Fund?”
    • “List top 5 holdings of the Consumption Fund with weights”
    • “Compare the allocation between equity and debt.”
    • “How has AUM changed compared to last month?”
    • “Which of the listed equity funds has the highest 3-year return?”
    • “State the YTM, Macaulay Duration and Average Maturity for the Money Market Fund”

Expected Features
    • RAG Pipeline: Use embeddings and vector search to retrieve relevant content.
    • Multimodal Capability: Handle text, tables, and charts (using OCR if needed).
    • Computation Layer: Perform calculations using data extracted from the PDF.
    • Chat Interface: Create a simple and interactive chat UI.
    • Answer Grounding: Show or cite the source section used for each answer.
    • Context-Aware Questions: The chatbot should handle follow-up questions smoothly.




Evaluation Criteria

Criteria
Description
Weight
Accuracy & Relevance
How correct and relevant are the answers?
30%
Architecture Design
How well is the RAG pipeline and retrieval logic implemented?
25%
User Experience
Clarity, usability, and look of the chatbot UI
15%
Handling Complex Data
How well it reads tables, performs calculations, or interprets charts
20%
Innovation & Optimization
Creativity, optimization, or unique features added
10%

Technical Guidelines
    • Input: PDF file - Bajaj AMC Fund Factsheet (Oct 2025)
    • Recommended Tech Stack:
        ◦ Backend: Python (LangChain / LlamaIndex / Haystack)
        ◦ Embeddings: OpenAI / Azure / AWS Bedrock / Hugging Face
        ◦ Vector Database: FAISS / Pinecone / Chroma
        ◦ Frontend: Streamlit / Angular / React
    • LLM Rule: The chatbot must only use facts from the PDF. If the question is outside the document, it should politely say so.

Deliverables
    1. Working Chatbot App (UI + Backend)
    2. Source Code with README and setup steps
    3. Short Demo Video (2–3 mins) showing:
        ◦ How the factsheet is uploaded
        ◦ Example queries and responses
        ◦ How it handles calculations and references

Bonus Points
    • Support for multiple factsheets (compare across months)
    • Visual responses - show charts or tables in replies
    • Confidence scores or source highlighting in answers

