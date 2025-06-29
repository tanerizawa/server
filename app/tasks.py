# backend/app/tasks.py

from app.celery_app import celery_app
from app.services.profile_analyzer_service import profile_analyzer
from app.db.session import SessionLocal
from app import crud

@celery_app.task
def analyze_profile_task(user_id: int):
    """
    Tugas Celery untuk menganalisis profil pengguna.
    """
    db = SessionLocal()
    try:
        user = crud.user.get(db, id=user_id)
        if user:
            profile_analyzer.analyze_and_update_profile(db=db, user=user)
    finally:
        db.close()
    return f"Profile analysis complete for user_id {user_id}"
