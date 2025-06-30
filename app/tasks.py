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

import asyncio
from app.services.quote_generation_service import QuoteGenerationService
from app.schemas.motivational_quote import MotivationalQuoteCreate
from app import models

@celery_app.task
def generate_quote_task():
    """Generate a motivational quote based on the latest journal mood."""
    db = SessionLocal()
    try:
        latest = db.query(models.Journal).order_by(models.Journal.created_at.desc()).first()
        mood = latest.mood if latest and latest.mood else "Netral"
        service = QuoteGenerationService()
        text, author = asyncio.run(service.generate_quote(mood))
        if text:
            crud.motivational_quote.create(
                db,
                obj_in=MotivationalQuoteCreate(text=text, author=author),
            )
    finally:
        db.close()
    return "Quote generation complete"
