from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import uuid
from pathlib import Path
import shutil
import librosa
import soundfile as sf
import numpy as np
from scipy import signal
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Audio Splitter API", version="1.0.0")

# CORS - Allow all origins for development
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

# Mount static files for serving separated audio (after directories are created)
try:
    app.mount("/files", StaticFiles(directory="processed"), name="files")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")

def separate_audio_simple(input_path, output_dir):
    """
    Simple frequency-based audio separation
    Separates vocals (mid frequencies) from instruments (other frequencies)
    """
    logger.info(f"Loading audio file: {input_path}")
    
    # Load audio
    y, sr = librosa.load(input_path, sr=44100, mono=False)
    
    # Convert to mono if stereo
    if len(y.shape) > 1:
        y = librosa.to_mono(y)
    
    logger.info("Separating audio using frequency analysis...")
    
    # Vocals (mid frequencies: 200Hz - 3000Hz)
    sos_vocals = signal.butter(4, [200, 3000], 'bandpass', fs=sr, output='sos')
    vocals = signal.sosfilt(sos_vocals, y)
    
    # Instruments (everything else)
    instruments = y - vocals
    
    # Normalize
    vocals = vocals / np.max(np.abs(vocals) + 1e-6) * 0.9
    instruments = instruments / np.max(np.abs(instruments) + 1e-6) * 0.9
    
    # Save files
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    vocals_path = output_dir / "vocals.wav"
    instruments_path = output_dir / "accompaniment.wav"
    
    logger.info(f"Saving vocals to: {vocals_path}")
    sf.write(str(vocals_path), vocals, sr)
    
    logger.info(f"Saving instruments to: {instruments_path}")
    sf.write(str(instruments_path), instruments, sr)
    
    return str(vocals_path), str(instruments_path)

@app.on_event("startup")
async def startup_event():
    """Ensure directories exist on startup"""
    UPLOAD_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    logger.info("Directories created successfully")

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
    Separate audio into vocals and instruments using Spleeter AI
    """
    try:
        # Validate file type
        if not audio.filename.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
            raise HTTPException(status_code=400, detail="Invalid audio format. Supported: mp3, wav, flac, m4a")
        
        # Generate unique ID for this separation job
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_extension = Path(audio.filename).suffix
        input_path = UPLOAD_DIR / f"{job_id}{file_extension}"
        
        logger.info(f"Saving uploaded file: {input_path}")
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
        
        # Create output directory for this job
        output_dir = PROCESSED_DIR / job_id
        output_dir.mkdir(exist_ok=True)
        
        # Separate audio using frequency-based method
        logger.info(f"Starting separation for job {job_id}")
        vocals_path_str, instruments_path_str = separate_audio_simple(str(input_path), str(output_dir))
        
        vocals_path = Path(vocals_path_str)
        accompaniment_path = Path(instruments_path_str)
        
        if not vocals_path.exists() or not accompaniment_path.exists():
            raise HTTPException(status_code=500, detail="Separation failed - output files not created")
        
        logger.info(f"Separation completed for job {job_id}")
        
        # Clean up input file
        input_path.unlink()
        
        # Get base URL from environment or use default
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        
        return {
            "success": True,
            "job_id": job_id,
            "vocals_url": f"{base_url}/files/{job_id}/vocals.wav",
            "instruments_url": f"{base_url}/files/{job_id}/accompaniment.wav",
            "other_url": f"{base_url}/files/{job_id}/accompaniment.wav",  # For compatibility
            "message": "Audio separated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error during separation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Separation failed: {str(e)}")

@app.delete("/api/cleanup/{job_id}")
async def cleanup_job(job_id: str):
    """
    Clean up processed files for a job
    """
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
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
