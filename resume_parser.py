import docx
import PyPDF2
import io

# Function for extracting content from a PDF resume
def extract_text_from_pdf(pdf_file):
    """Extracts text from a file-like PDF object"""
    reader = PyPDF2.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Function for extracting content from a DOCX resume
def extract_text_from_docx(docx_file):
    """Extracts text from a file-like DOCX object"""
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(file_obj, file_type):
    """Extracts text based on file format"""
    if file_type == "application/pdf":
        return extract_text_from_pdf(file_obj)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_obj)
    else:
        raise ValueError("Unsupported file format. Please upload a .pdf or .docx file.")
