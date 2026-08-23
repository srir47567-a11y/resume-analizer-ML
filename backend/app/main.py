"""
SkillMatch ML - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from backend.app.api.resume import router as resume_router
from backend.app.api.prediction import router as prediction_router
from backend.app.api.matching import router as matching_router

app = FastAPI(
    title="SkillMatch ML",
    description="ML-powered Resume Intelligence & Job Matching System for Students and Freshers",
    version="1.0.0"
)

# Enable CORS for local and web development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(resume_router)
app.include_router(prediction_router)
app.include_router(matching_router)

# Health endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "SkillMatch ML Engine",
        "version": "1.0.0"
    }

# Mount Frontend static files
frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

    @app.get("/")
    async def serve_index():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "SkillMatch ML API is running. Frontend index.html not found."}
