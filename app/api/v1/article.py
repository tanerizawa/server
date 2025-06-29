from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.dependencies import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.Article])
def get_articles(db: Session = Depends(get_db)):
    return crud.article.get_multi(db)
