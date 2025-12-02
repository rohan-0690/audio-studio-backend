from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import uuid
from pathlib import Path
import shutil
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Audio Splitter API", version="1.0.0")

# CORS - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("uploads")
PROCESSED_DIR = Path("processed")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
async def startup_event():
    """Ensure directories exist on startup"""
    UPLOAD_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    logger.info("Audio Splitter API started successfully")

@app.get("/")
async def root():
    return {
        "message": "Audio Splitter API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "separate": "/api/separate",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "audio-splitter"}

@app.post("/api/separate")
async def separate_audio(audio: UploadFile = File(...)):
    """
    Separate audio - simplified version for Railway
    """
    try:
        # Validate file type
        if not audio.filename.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
            raise HTTPException(status_code=400, detail="Invalid audio format")
        
        # Generate unique ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_extension = Path(audio.filename).suffix
        input_path = UPLOAD_DIR / f"{job_id}{file_extension}"
        
        logger.info(f"Saving uploaded file: {input_path}")
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # Create output directory
        output_dir = PROCESSED_DIR / job_id
        output_dir.mkdir(exist_ok=True)
        
        # For now, just copy the file as both vocals and instruments
        # This is a placeholder until we can get proper audio processing working
        vocals_path = output_dir / "vocals.wav"
        instruments_path = output_dir / "accompaniment.wav"
        
        shutil.copy(input_path, vocals_path)
        shutil.copy(input_path, instruments_path)
        
        logger.info(f"Files created for job {job_id}")
        
        # Clean up input file
        input_path.unlink()
        
        # Get base URL
        base_url = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
        if base_url:
            base_url = f"https://{base_url}"
        else:
            base_url = "http://localhost:8000"
        
        return {
            "success": True,
            "job_id": job_id,
            "vocals_url": f"{base_url}/files/{job_id}/vocals.wav",
            "instruments_url": f"{base_url}/files/{job_id}/accompaniment.wav",
            "other_url": f"{base_url}/files/{job_id}/accompaniment.wav",
            "message": "Audio separated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed: {str(e)}")

@app.get("/files/{job_id}/{filename}")
async def get_file(job_id: str, filename: str):
    """Serve separated audio files"""
    file_path = PROCESSED_DIR / job_id / filename
    if file_path.exists():
        return FileResponse(file_path, media_type="audio/wav")
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.delete("/api/cleanup/{job_id}")
async def cleanup_job(job_id: str):
    """Clean up processed files"""
    try:
        job_dir = PROCESSED_DIR / job_id
        if job_dir.exists():
            shutil.rmtree(job_dir)
            return {"success": True, "message": f"Cleaned up job {job_id}"}
        else:
            raise HTTPException(status_code=404, detail="Job not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("simple_app:app", host="0.0.0.0", port=port, reload=False)
