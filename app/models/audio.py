from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class AudioTrack(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String)
