"""
Resume Parser Service for extracting text and structured sections from PDF, DOCX, and raw text.
"""

import io
import re
from typing import Dict, Any, List, Optional
from pypdf import PdfReader
import docx

from backend.app.utils.text_cleaner import clean_raw_text

# Regex patterns for identifying standard resume section headers
SECTION_PATTERNS = {
    "summary": re.compile(r'^(?:professional\s+summary|summary|profile|about\s+me|career\s+objective|objective)\b', re.IGNORECASE),
    "skills": re.compile(r'^(?:technical\s+skills|skills\s*&\s*abilities|skills|core\s+competencies|technologies|tools\s*&\s*technologies|key\s+skills)\b', re.IGNORECASE),
    "experience": re.compile(r'^(?:work\s+experience|experience|employment\s+history|professional\s+experience|internships?|work\s+history)\b', re.IGNORECASE),
    "projects": re.compile(r'^(?:projects|academic\s+projects|personal\s+projects|key\s+projects|notable\s+projects)\b', re.IGNORECASE),
    "education": re.compile(r'^(?:education|academic\s+background|educational\s+qualifications|academics|qualifications)\b', re.IGNORECASE),
    "certifications": re.compile(r'^(?:certifications?|certificates?|licenses?|courses?|achievements?|awards?|honors?)\b', re.IGNORECASE)
}

class ResumeParser:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extracts text from PDF binary stream using pypdf."""
        reader = PdfReader(io.BytesIO(file_bytes))
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "\n".join(pages_text)

    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        """Extracts text from DOCX binary stream using python-docx."""
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    def extract_contact_info(self, raw_text: str) -> Dict[str, Optional[str]]:
        """Extracts candidate email, phone, and profile links from resume text."""
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', raw_text)
        email = email_match.group(0) if email_match else None

        # Phone
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', raw_text)
        phone = phone_match.group(0) if phone_match else None

        # Links (LinkedIn, GitHub, Portfolio)
        linkedin_match = re.search(r'(?:linkedin\.com/in/|linkedin:\s*)([A-Za-z0-9_-]+)', raw_text, re.IGNORECASE)
        linkedin = linkedin_match.group(0) if linkedin_match else None

        github_match = re.search(r'(?:github\.com/|github:\s*)([A-Za-z0-9_-]+)', raw_text, re.IGNORECASE)
        github = github_match.group(0) if github_match else None

        return {
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github
        }

    def detect_sections(self, raw_text: str) -> Dict[str, str]:
        """
        Splits resume text into semantic sections: summary, skills, experience, projects, education, certifications.
        """
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        sections: Dict[str, List[str]] = {
            "summary": [],
            "skills": [],
            "experience": [],
            "projects": [],
            "education": [],
            "certifications": [],
            "other": []
        }

        current_section = "summary"

        for line in lines:
            # Check if this line matches a section heading
            matched_section = None
            # Section headers are usually short (less than 40 chars)
            if len(line) < 40:
                clean_line = re.sub(r'[:#*_\-]', '', line).strip()
                for section_name, pattern in SECTION_PATTERNS.items():
                    if pattern.match(clean_line):
                        matched_section = section_name
                        break

            if matched_section:
                current_section = matched_section
            else:
                sections[current_section].append(line)

        # Join lines for each section
        return {
            sec: "\n".join(content_lines).strip()
            for sec, content_lines in sections.items()
            if content_lines
        }

    def parse(self, raw_text: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Main parse method converting raw text to a structured resume object.
        """
        cleaned_text = clean_raw_text(raw_text)
        contact_info = self.extract_contact_info(raw_text)
        sections = self.detect_sections(raw_text)

        # Determine estimated word and character count
        word_count = len(cleaned_text.split())
        char_count = len(cleaned_text)

        return {
            "filename": filename or "resume.txt",
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "word_count": word_count,
            "char_count": char_count,
            "contact_info": contact_info,
            "sections": sections
        }

# Global singleton instance
resume_parser = ResumeParser()
