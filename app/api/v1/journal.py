# backend/app/api/v1/journal.py (Versi Perbaikan)

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.dependencies import get_db, get_current_user
from app.tasks import analyze_profile_task
import structlog

router = APIRouter()
log = structlog.get_logger(__name__)


@router.post("/", response_model=schemas.JournalInDB)
def create_journal(
        *,
        db: Session = Depends(get_db),
        journal_in: schemas.JournalCreate,
        current_user: models.User = Depends(get_current_user),
        background_tasks: BackgroundTasks,
):
    if not journal_in.content.strip():
        raise HTTPException(status_code=400, detail="Konten jurnal tidak boleh kosong.")

    journal = crud.journal.create_with_owner(db=db, obj_in=journal_in, owner_id=current_user.id)

    background_tasks.add_task(analyze_profile_task, current_user.id)

    log.info(
        "Jurnal dibuat",
        user_id=current_user.id,
        journal_id=journal.id,
    )

    return journal

@router.get("/", response_model=list[schemas.JournalInDB])
def read_journals(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(get_current_user),
):
    limit = min(limit, 100)
    journals = crud.journal.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit, order_by="created_at desc"
    )

    # --- PERBAIKAN DI SINI ---
    # Secara eksplisit menangani kasus di mana tidak ada jurnal yang ditemukan
    # dan langsung mengembalikan daftar kosong untuk mencegah error lebih lanjut.
    if not journals:
        return []

    return journals

