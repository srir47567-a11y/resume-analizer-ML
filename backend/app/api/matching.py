"""
Matching API Router: Job Description matching, skill gap analysis, and learning roadmaps.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from backend.app.services.matcher import job_matcher
from backend.app.services.roadmap import roadmap_generator
from backend.app.services.resume_parser import resume_parser
from backend.app.services.skill_extractor import skill_extractor
from backend.app.ml.predict import role_classifier_service

router = APIRouter(prefix="/api", tags=["Job Matching & Roadmap"])

class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str
    target_role: Optional[str] = None
    sections: Optional[Dict[str, str]] = None

class RoadmapRequest(BaseModel):
    current_skills: List[str]
    missing_skills: List[Dict[str, Any]]
    target_role: Optional[str] = "Target Role"
    overall_match_score: Optional[float] = 0.0

class FullAnalysisRequest(BaseModel):
    resume_text: str
    job_description: Optional[str] = None
    target_role: Optional[str] = None

@router.post("/match-job")
async def match_job(request: JobMatchRequest):
    """
    Compares resume with job description, calculates similarity and returns matched/missing skills.
    """
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")
    if not request.job_description.strip():
        raise HTTPException(status_code=400, detail="Job description text is required.")

    match_result = job_matcher.match(
        request.resume_text,
        request.job_description,
        request.sections
    )

    return {
        "success": True,
        **match_result
    }

@router.post("/roadmap")
async def generate_learning_roadmap(request: RoadmapRequest):
    """
    Generates prioritized skill gaps and sequential learning roadmap.
    """
    roadmap = roadmap_generator.generate_roadmap(
        request.current_skills,
        request.missing_skills,
        request.target_role or "Target Role",
        request.overall_match_score or 0.0
    )

    return {
        "success": True,
        **roadmap
    }

@router.post("/analyze-full")
async def analyze_full_pipeline(request: FullAnalysisRequest):
    """
    Executes the entire SkillMatch ML pipeline:
    1. Parse resume structure & extract contact info
    2. Extract and canonicalize candidate skills
    3. Predict job role with ML probabilities
    4. (Optional) Compare with Job Description, calculate similarity, skill gaps & roadmap
    """
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")

    # 1. Parse Resume
    parsed = resume_parser.parse(request.resume_text)
    
    # 2. Extract Skills
    resume_skills = skill_extractor.extract_skills(request.resume_text, parsed["sections"])
    
    # 3. Predict Role
    ml_prediction = role_classifier_service.predict_roles(request.resume_text, top_k=4)
    top_predicted_role = ml_prediction.get("top_role", "Software Developer")

    # 4. Job Match & Roadmap (if JD provided)
    match_data = None
    roadmap_data = None
    
    if request.job_description and request.job_description.strip():
        target_role = request.target_role or top_predicted_role
        match_data = job_matcher.match(request.resume_text, request.job_description, parsed["sections"])
        
        current_skill_names = [s["name"] for s in resume_skills]
        roadmap_data = roadmap_generator.generate_roadmap(
            current_skills=current_skill_names,
            missing_skills=match_data["missing_skills"],
            target_role=target_role,
            overall_match_score=match_data["overall_match_score"]
        )

    return {
        "success": True,
        "parsed_resume": {
            "contact_info": parsed["contact_info"],
            "word_count": parsed["word_count"],
            "sections": parsed["sections"]
        },
        "skills": resume_skills,
        "role_prediction": ml_prediction,
        "job_match": match_data,
        "roadmap": roadmap_data
    }
