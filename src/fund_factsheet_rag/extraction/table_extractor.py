import pdfplumber

def extract_tables_from_pdf(pdf_path: str):
    """Extracts tables from PDF pages."""
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            for table in page.extract_tables():
                tables.append({"page": i + 1, "table": table})
    return tables
