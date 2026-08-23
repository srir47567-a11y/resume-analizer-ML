"""
Resume API Router: Handles resume uploads (PDF/DOCX/TXT) and text parsing.
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.app.services.resume_parser import resume_parser
from backend.app.services.skill_extractor import skill_extractor

router = APIRouter(prefix="/api/resume", tags=["Resume"])

@router.post("/upload")
async def upload_resume(
    file: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None)
):
    """
    Accepts resume file (PDF/DOCX/TXT) or raw text input and extracts structured information.
    """
    extracted_text = ""
    filename = "resume.txt"

    if file:
        filename = file.filename
        content = await file.read()
        
        if filename.lower().endswith(".pdf"):
            try:
                extracted_text = resume_parser.extract_text_from_pdf(content)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {str(e)}")
        elif filename.lower().endswith(".docx"):
            try:
                extracted_text = resume_parser.extract_text_from_docx(content)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to extract DOCX text: {str(e)}")
        elif filename.lower().endswith(".txt"):
            try:
                extracted_text = content.decode("utf-8", errors="ignore")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Failed to read TXT file: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOCX, or TXT.")

    elif raw_text:
        extracted_text = raw_text.strip()
    else:
        raise HTTPException(status_code=400, detail="Please upload a resume file or provide resume text.")

    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No readable text could be extracted from the provided resume.")

    # Parse sections and contact info
    parsed_resume = resume_parser.parse(extracted_text, filename=filename)
    
    # Extract skills
    skills = skill_extractor.extract_skills(extracted_text, parsed_resume["sections"])
    
    return {
        "success": True,
        "filename": filename,
        "contact_info": parsed_resume["contact_info"],
        "word_count": parsed_resume["word_count"],
        "char_count": parsed_resume["char_count"],
        "sections": parsed_resume["sections"],
        "skills": skills,
        "raw_text": extracted_text
    }
