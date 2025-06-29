# backend/app/crud/crud_journal.py (Versi Perbaikan)

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.journal import Journal
from app.schemas.journal import JournalCreate, JournalUpdate
from sqlalchemy import desc # Pastikan `desc` diimpor

class CRUDJournal(CRUDBase[Journal, JournalCreate, JournalUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: JournalCreate, owner_id: int
    ) -> Journal:
        db_obj = Journal(**obj_in.model_dump(), owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100, order_by: str = None
    ) -> list[Journal]:
        # --- PERBAIKAN DI SINI ---
        # Membangun query secara bertahap untuk stabilitas
        query = db.query(self.model).filter(self.model.owner_id == owner_id)

        # Menerapkan pengurutan hanya jika diminta
        if order_by == "created_at desc":
            query = query.order_by(desc(self.model.created_at))

        # Menerapkan limit dan offset
        journals = query.offset(skip).limit(limit).all()

        return journals

journal = CRUDJournal(Journal)
