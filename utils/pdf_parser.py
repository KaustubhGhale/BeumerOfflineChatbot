import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def extract_text_from_pdf(file_path):
    try:
        text = ''
        tables = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + '\n'
                page_tables = page.extract_tables()
                for table in page_tables:
                    tables.append(table)
        if text.strip():
            return text.strip(), tables

        # OCR fallback
        text = ''
        images = convert_from_path(file_path)
        for image in images:
            text += pytesseract.image_to_string(image)
        return text.strip(), []

    except Exception as e:
        print("PDF Parsing Error:", e)
        return "", []
