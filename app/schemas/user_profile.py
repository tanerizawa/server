# backend/app/schemas/user_profile.py

from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional
from datetime import datetime

class UserProfileBase(BaseModel):
    emerging_themes: Optional[Dict[str, float]] = None
    sentiment_trend: Optional[str] = None

class UserProfileUpdate(UserProfileBase):
    """Schema untuk update data profil pengguna (partial update)."""
    pass

class UserProfile(UserProfileBase):
    """Schema umum untuk konsumsi eksternal (misal: di API response)."""
    id: int
    user_id: int
    last_analyzed: datetime

    model_config = ConfigDict(from_attributes=True)

class UserProfileInDB(UserProfile):
    """Schema untuk penggunaan internal, jika ingin dipisahkan (opsional)."""
    pass
