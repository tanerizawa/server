from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.AudioTrack])
def get_audio(db: Session = Depends(get_db)):
    return crud.audio_track.get_multi(db)
