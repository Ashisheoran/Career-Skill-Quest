# resume_parser.py
import fitz  # PyMuPDF
from docx import Document
import re
from typing import Dict, List, Any
from models.pydantic_models import ResumeData

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """Extracts text from PDF content."""
    text = ""
    try:
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(docx_content: bytes) -> str:
    """Extracts text from DOCX content."""
    text = ""
    try:
        doc = Document(docx_content)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text

def parse_resume(file_content: bytes, file_type: str) -> ResumeData:
    """
    Parses resume content (PDF or DOCX) and extracts key information.
    This is a basic parser. For production, consider more advanced NLP.
    """
    text = ""
    if file_type == "pdf":
        text = extract_text_from_pdf(file_content)
    elif file_type == "docx":
        text = extract_text_from_docx(file_content)
    else:
        raise ValueError("Unsupported file type")

    # Basic extraction using regex and keyword matching
    name = "N/A"
    email = "N/A"
    experience = "N/A"
    education = "N/A"
    skills = []
    experience_years = 0

    # Name: Often at the top, can be difficult to reliably extract without NLP
    lines = text.split('\n')
    if lines:
        # Heuristic: Prioritize lines with multiple capitalized words, then fall back to first non-empty line
        for line in lines[:5]: # Check first few lines
            if line.strip() and len(line.strip().split()) > 1 and all(word.istitle() or not word.isalpha() for word in line.strip().split()):
                name = line.strip()
                break
        if name == "N/A" and lines[0].strip():
            name = lines[0].strip()

    # Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        email = email_match.group(0)

    # Experience
    experience_match = re.search(
        r"(experience|work history|professional experience)\s*(\n|:)(.*?)(education|skills|achievements|projects|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    if experience_match:
        experience = experience_match.group(3).strip()
        # Try to extract years of experience if present
        years_match = re.search(r"(\d+)\s*(year|yr)s?\s*of\s*(experience|exp)", experience, re.IGNORECASE)
        if years_match:
            experience_years = int(years_match.group(1))
        else:
            # Fallback: estimate from common phrases if direct years not found
            if re.search(r"(\d+)\+\s*years", experience, re.IGNORECASE):
                experience_years = int(re.search(r"(\d+)", experience).group(1))
            elif re.search(r"junior|entry-level", experience, re.IGNORECASE):
                experience_years = 0
            elif re.search(r"senior|lead|principal", experience, re.IGNORECASE):
                experience_years = 5 # Arbitrary, adjust as needed

    # Education
    education_match = re.search(
        r"(education|qualifications)\s*(\n|:)(.*?)(skills|experience|projects|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    if education_match:
        education = education_match.group(3).strip()

    # Skills - Improved extraction, looking for common skill section headings
    skills_match = re.search(
        r"(skills|technical skills|proficiencies|core competencies)\s*(\n|:)(.*?)(experience|education|projects|awards|$)",
        text, re.IGNORECASE | re.DOTALL
    )
    if skills_match:
        skills_text = skills_match.group(3).strip()
        # Split by common delimiters: commas, newlines, bullet points, etc.
        raw_skills = re.split(r'[,;\n\u2022-]', skills_text) # \u2022 is bullet point character
        skills = [s.strip() for s in raw_skills if s.strip() and len(s.strip()) > 1]
        # Further refine skills (e.g., remove common filler words, ensure uniqueness)
        skills = list(set([s.lower() for s in skills])) # Convert to lowercase and get unique

    # Basic cleanup for extracted text fields
    experience = re.sub(r'\s+', ' ', experience).strip()
    education = re.sub(r'\s+', ' ', education).strip()

    return ResumeData(
        name=name,
        email=email,
        experience=experience,
        experience_years=experience_years,
        education=education,
        skills=skills
    )