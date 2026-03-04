import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file.
    """
    if not os.path.exists(pdf_path):
        return "Error: File not found."
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test script
    print("PDF Processor Tool Loaded.")
