from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.security import create_access_token, verify_password
from app.dependencies import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserPublic)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
):
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/login", response_model=schemas.Token)
def login(
    *,
    db: Session = Depends(get_db),
    login_in: schemas.UserLogin,
):
    user = crud.user.get_by_email(db, email=login_in.email)
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
