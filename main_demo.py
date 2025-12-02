from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI(title="AI Audio Studio API - Demo Mode", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
Path("uploads").mkdir(exist_ok=True)
Path("processed").mkdir(exist_ok=True)

# In-memory storage for demo
users_db = {}
projects_db = {}
recordings_db = {}

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class EffectParams(BaseModel):
    effect_type: str
    eq_bands: Optional[list] = None
    compression_ratio: Optional[float] = None
    reverb_room_size: Optional[float] = None
    reverb_damping: Optional[float] = None

class DrumParams(BaseModel):
    genre: str
    bpm: Optional[int] = None
    duration: int = 8

@app.get("/")
async def root():
    return {
        "message": "AI Audio Studio API - Demo Mode",
        "version": "1.0.0",
        "status": "running",
        "note": "Running in demo mode without database"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "demo"}

# Auth endpoints
@app.post("/api/auth/register")
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users_db[user.email] = {
        "email": user.email,
        "username": user.username,
        "id": len(users_db) + 1
    }
    
    return {
        "access_token": f"demo_token_{user.email}",
        "token_type": "bearer"
    }

@app.post("/api/auth/login")
async def login(username: str, password: str):
    # Demo mode - accept any credentials
    return {
        "access_token": f"demo_token_{username}",
        "token_type": "bearer"
    }

# Audio processing endpoints
@app.post("/api/audio/upload")
async def upload_audio(file: UploadFile = File(...)):
    recording_id = len(recordings_db) + 1
    recordings_db[recording_id] = {
        "id": recording_id,
        "filename": file.filename,
        "duration": 30.5,
        "sample_rate": 44100,
        "channels": 1
    }
    
    return {
        "recording_id": recording_id,
        "filename": file.filename,
        "duration": 30.5,
        "metadata": {
            "duration": 30.5,
            "sample_rate": 44100,
            "channels": 1,
            "bit_depth": 16
        }
    }

@app.post("/api/audio/noise-cancel/{recording_id}")
async def apply_noise_cancellation(recording_id: int):
    if recording_id not in recordings_db:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return {
        "message": "Noise cancellation applied successfully",
        "recording_id": recording_id
    }

@app.post("/api/audio/apply-effects/{recording_id}")
async def apply_effects(recording_id: int, params: EffectParams):
    if recording_id not in recordings_db:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return {
        "message": f"{params.effect_type} applied successfully",
        "recording_id": recording_id,
        "effect": params.effect_type
    }

@app.post("/api/audio/split-stems/{recording_id}")
async def split_stems(recording_id: int):
    if recording_id not in recordings_db:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return {
        "message": "Stems separated successfully",
        "stems": {
            "vocals": f"processed/vocals_{recording_id}.wav",
            "drums": f"processed/drums_{recording_id}.wav",
            "bass": f"processed/bass_{recording_id}.wav",
            "other": f"processed/other_{recording_id}.wav"
        }
    }

@app.post("/api/audio/generate-drums")
async def generate_drums(params: DrumParams):
    return {
        "message": "Drums generated successfully",
        "genre": params.genre,
        "bpm": params.bpm or 120,
        "duration": params.duration,
        "file": f"processed/drums_{params.genre}.wav"
    }

@app.get("/api/audio/detect-bpm/{recording_id}")
async def detect_bpm(recording_id: int):
    if recording_id not in recordings_db:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return {"bpm": 120}

# Project endpoints
@app.get("/api/projects/")
async def get_projects():
    return list(projects_db.values())

@app.post("/api/projects/")
async def create_project(project: ProjectCreate):
    project_id = len(projects_db) + 1
    projects_db[project_id] = {
        "id": project_id,
        "name": project.name,
        "description": project.description,
        "created_at": "2025-11-07T12:00:00"
    }
    return projects_db[project_id]

@app.get("/api/projects/{project_id}")
async def get_project(project_id: int):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project": projects_db[project_id],
        "recordings": [r for r in recordings_db.values()]
    }

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: int):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    del projects_db[project_id]
    return {"message": "Project deleted successfully"}

if __name__ == "__main__":
    print("=" * 60)
    print("🎵 AI AUDIO STUDIO - DEMO MODE")
    print("=" * 60)
    print("✅ Backend server starting...")
    print("📍 API URL: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("⚠️  Running in DEMO mode (no database required)")
    print("=" * 60)
    uvicorn.run("main_demo:app", host="0.0.0.0", port=8000, reload=True)
