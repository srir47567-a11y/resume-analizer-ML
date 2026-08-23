"""
Utility to generate sample PDF and DOCX resume files for manual and automated verification.
"""

from pathlib import Path
from pypdf import PdfWriter
import docx

def create_sample_docx(filepath: Path):
    doc = docx.Document()
    doc.add_heading('John Doe - Junior Python Backend Developer', 0)
    
    doc.add_paragraph('Email: john.doe@example.com | Phone: +1 555-019-2834 | GitHub: github.com/johndoe')
    
    doc.add_heading('Professional Summary', level=1)
    doc.add_paragraph(
        'Passionate Python Backend Developer with hands-on experience in FastAPI, PostgreSQL, '
        'Redis, and building scalable RESTful APIs with Docker and automated Pytest testing.'
    )
    
    doc.add_heading('Technical Skills', level=1)
    doc.add_paragraph('Python, FastAPI, Django, Flask, PostgreSQL, SQL, Redis, Docker, Git, Pytest, REST API, Linux')
    
    doc.add_heading('Projects', level=1)
    doc.add_paragraph(
        '1. High-Throughput E-Commerce API (FastAPI, PostgreSQL, Redis):\n'
        '   - Developed asynchronous REST API with JWT authentication and Redis caching.\n'
        '   - Containerized application with Docker Compose for seamless local development.\n'
        '2. Real-Time Chat WebSocket Service (Python, Redis Pub/Sub):\n'
        '   - Built WebSocket server handling 500+ concurrent connections.'
    )
    
    doc.add_heading('Education', level=1)
    doc.add_paragraph('B.Tech in Computer Science and Engineering (2020 - 2024)')
    
    doc.save(str(filepath))
    print(f"Saved DOCX sample to {filepath}")

def main():
    sample_dir = Path("sample_resumes")
    sample_dir.mkdir(exist_ok=True)
    
    create_sample_docx(sample_dir / "sample_python_developer.docx")

if __name__ == "__main__":
    main()
