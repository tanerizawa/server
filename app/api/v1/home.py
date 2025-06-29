from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()

@router.get("/home-feed")
def get_home_feed(db: Session = Depends(get_db)):
    """Return combined recent content for the home screen."""
    articles = crud.article.get_multi(db)
    audio_tracks = crud.audio_track.get_multi(db)
    quotes = crud.motivational_quote.get_multi(db)

    items = []
    for obj in articles:
        items.append({"type": "article", "data": schemas.Article.model_validate(obj)})
    for obj in audio_tracks:
        items.append({"type": "audio", "data": schemas.AudioTrack.model_validate(obj)})
    for obj in quotes:
        items.append({"type": "quote", "data": schemas.MotivationalQuote.model_validate(obj)})

    items.sort(key=lambda x: x["data"].id, reverse=True)
    return items
