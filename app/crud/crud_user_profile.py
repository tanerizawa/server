# backend/app/crud/crud_user_profile.py

from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileUpdate

class CRUDUserProfile(CRUDBase[UserProfile, None, UserProfileUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> UserProfile | None:
        """Mengambil profil berdasarkan ID pengguna."""
        return db.query(self.model).filter(self.model.user_id == user_id).first()

    def create_with_user(self, db: Session, *, user_id: int) -> UserProfile:
        """Membuat profil kosong untuk pengguna baru."""
        db_obj = UserProfile(user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_profile = CRUDUserProfile(UserProfile)