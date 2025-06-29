from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.MotivationalQuote])
def get_quotes(db: Session = Depends(get_db)):
    return crud.motivational_quote.get_multi(db)
