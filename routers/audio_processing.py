from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import os
import uuid
from pathlib import Path

from database import get_db
from models import Recording, EffectLog, User
from routers.auth import get_current_user
from services.audio_processor import AudioProcessor
from services.noise_cancellation import NoiseCanceller
from services.stem_separator import StemSeparator
from services.drum_machine import DrumMachine

router = APIRouter()
audio_processor = AudioProcessor()
noise_canceller = NoiseCanceller()
stem_separator = StemSeparator()
drum_machine = DrumMachine()

class EffectParams(BaseModel):
    effect_type: str
    eq_bands: Optional[List[float]] = None
    compression_ratio: Optional[float] = None
    reverb_room_size: Optional[float] = None
    reverb_damping: Optional[float] = None

class DrumParams(BaseModel):
    genre: str
    bpm: Optional[int] = None
    duration: int = 8

@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    project_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.wav', '.mp3', '.m4a', '.flac')):
        raise HTTPException(status_code=400, detail="Invalid audio format")
    
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = f"uploads/{file_id}{file_extension}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Get audio metadata
    metadata = audio_processor.get_metadata(file_path)
    
    recording = Recording(
        project_id=project_id,
        filename=file.filename,
        file_path=file_path,
        duration=metadata['duration'],
        sample_rate=metadata['sample_rate'],
        channels=metadata['channels'],
        format=file_extension[1:]
    )
    db.add(recording)
    db.commit()
    db.refresh(recording)
    
    return {
        "recording_id": recording.id,
        "filename": recording.filename,
        "duration": recording.duration,
        "metadata": metadata
    }

@router.post("/noise-cancel/{recording_id}")
async def apply_noise_cancellation(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    output_path = f"processed/{uuid.uuid4()}.wav"
    noise_canceller.process(recording.file_path, output_path)
    
    effect_log = EffectLog(
        recording_id=recording_id,
        effect_type="noise_cancellation",
        parameters="{}"
    )
    db.add(effect_log)
    db.commit()
    
    return FileResponse(output_path, media_type="audio/wav", filename="noise_cancelled.wav")

@router.post("/apply-effects/{recording_id}")
async def apply_effects(
    recording_id: int,
    params: EffectParams,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    output_path = f"processed/{uuid.uuid4()}.wav"
    
    if params.effect_type == "equalizer" and params.eq_bands:
        audio_processor.apply_equalizer(recording.file_path, output_path, params.eq_bands)
    elif params.effect_type == "compressor" and params.compression_ratio:
        audio_processor.apply_compressor(recording.file_path, output_path, params.compression_ratio)
    elif params.effect_type == "reverb":
        audio_processor.apply_reverb(
            recording.file_path, 
            output_path, 
            params.reverb_room_size or 0.5,
            params.reverb_damping or 0.5
        )
    elif params.effect_type == "ai_enhance":
        audio_processor.ai_enhance(recording.file_path, output_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid effect type")
    
    effect_log = EffectLog(
        recording_id=recording_id,
        effect_type=params.effect_type,
        parameters=params.model_dump_json()
    )
    db.add(effect_log)
    db.commit()
    
    return FileResponse(output_path, media_type="audio/wav")

@router.post("/split-stems/{recording_id}")
async def split_stems(
    recording_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    output_dir = f"processed/stems_{uuid.uuid4()}"
    stems = stem_separator.separate(recording.file_path, output_dir)
    
    return {
        "message": "Stems separated successfully",
        "stems": stems
    }

@router.post("/generate-drums")
async def generate_drums(
    params: DrumParams,
    current_user: User = Depends(get_current_user)
):
    output_path = f"processed/drums_{uuid.uuid4()}.wav"
    drum_machine.generate(params.genre, output_path, params.bpm, params.duration)
    
    return FileResponse(output_path, media_type="audio/wav", filename=f"drums_{params.genre}.wav")

@router.get("/detect-bpm/{recording_id}")
async def detect_bpm(
    recording_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    recording = db.query(Recording).filter(Recording.id == recording_id).first()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    bpm = audio_processor.detect_bpm(recording.file_path)
    return {"bpm": bpm}
