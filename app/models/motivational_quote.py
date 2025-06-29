from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class MotivationalQuote(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    author = Column(String)
