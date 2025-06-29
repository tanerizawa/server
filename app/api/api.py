from fastapi import APIRouter
from app.api.v1 import auth, journal, chat, user, article, audio, quote, home
from app.api.v1.music import router as music_router

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(journal.router, prefix="/journals", tags=["journals"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(user.router, tags=["users"])
api_router.include_router(article.router, prefix="/articles", tags=["articles"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(quote.router, prefix="/quotes", tags=["quotes"])
api_router.include_router(home.router, tags=["home"])
api_router.include_router(music_router, prefix="/music", tags=["music"])

