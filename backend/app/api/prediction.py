"""
Prediction API Router: ML Role classification and model metrics.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import json
from pathlib import Path
from backend.app.ml.predict import role_classifier_service

router = APIRouter(prefix="/api", tags=["ML Prediction"])

class TextPredictionRequest(BaseModel):
    resume_text: str
    top_k: Optional[int] = 4

@router.post("/predict-role")
async def predict_role(request: TextPredictionRequest):
    """
    Predicts the most suitable job roles based on candidate resume text using the trained ML model.
    """
    if not request.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required for role prediction.")

    try:
        prediction_result = role_classifier_service.predict_roles(request.resume_text, top_k=request.top_k or 4)
        return {
            "success": True,
            **prediction_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@router.get("/models/evaluation")
async def get_model_evaluation():
    """
    Returns the comprehensive ML model benchmark and evaluation report.
    """
    report_path = Path("backend/app/models/evaluation_report.json")
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Evaluation report not found.")

    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "success": True,
        "evaluation": data
    }
