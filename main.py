from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from pathlib import Path
import shutil
from typing import Optional
import os

from routers import audio_processing, auth, projects
from database import engine, Base
from config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Audio Studio API", version="1.0.0")

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
Path("temp").mkdir(exist_ok=True)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(audio_processing.router, prefix="/api/audio", tags=["Audio Processing"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])

@app.get("/")
async def root():
    return {
        "message": "AI Audio Studio API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
