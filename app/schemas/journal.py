from pydantic import BaseModel, ConfigDict
from datetime import datetime

class JournalBase(BaseModel):
    title: str
    content: str
    mood: str

class JournalCreate(JournalBase):
    pass

class JournalUpdate(JournalBase):
    pass

class JournalInDB(JournalBase):
    id: int
    owner_id: int
    created_at: datetime
    sentiment_score: float | None = None
    sentiment_label: str | None = None

    model_config = ConfigDict(from_attributes=True)
