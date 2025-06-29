from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter()

@router.get("/users/me", response_model=schemas.UserPublic)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.delete("/users/me", response_model=schemas.UserPublic)
def delete_user_me(
    *,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user = crud.user.remove(db=db, id=current_user.id)
    return user
