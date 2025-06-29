from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.audio import AudioTrack
from app.schemas.audio import AudioTrackCreate, AudioTrackUpdate

class CRUDAudioTrack(CRUDBase[AudioTrack, AudioTrackCreate, AudioTrackUpdate]):
    pass

audio_track = CRUDAudioTrack(AudioTrack)
