import sys
import re
import fitz  # PyMuPDF
from docx import Document
import textract

def extract_text_from_pdf(pdf_path):
    # Open the provided PDF file
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    # Load the DOCX file
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_doc(doc_path):
    # Extract text from a DOC file using textract
    text = textract.process(doc_path).decode('utf-8')
    return text

def extract_email_and_phone(text):
    # Regular expressions for extracting emails and phone numbers
    email_regex = r"[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+\.[a-zA-Z0-9-_.]+"
    phone_regex = r"(?:\+?[0-9]{1,3}\s?)?(?:\(?[0-9]{3}\)?[-\s]?)[0-9]{3}[-\s]?[0-9]{4}"
    
    emails = re.findall(email_regex, text)
    phones = re.findall(phone_regex, text)
    
    # Extract unique emails and phones to avoid duplicates
    unique_emails = list(set(emails))
    unique_phones = list(set(phones))
    unique_phones=[i for i in unique_phones if len(i)>9 and len(i)<=13]
    
    return unique_emails, unique_phones

def process_cv(file_path):
    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.lower().endswith('.doc'):
        text = extract_text_from_doc(file_path)
    else:
        print("Unsupported file format")
        return []
    
    emails, phones = extract_email_and_phone(text)
    return [emails, phones, text]

# Example usage:
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_cv.py <path_to_cv>")
    else:
        result = process_cv(sys.argv[1])
        print("Emails:", result[0])
        print("Phones:", result[1])
        print("Text:", result[2][:1000])  # Print first 1000 characters of the text for brevity
