from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.user import User
import datetime

class Journal(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    mood = Column(String)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="journals")
User.journals = relationship("Journal", order_by=Journal.id, back_populates="owner")
