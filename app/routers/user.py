from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import user as schemas
from app.crud import user as crud
from ..dependency import get_db

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register", response_model=schemas.UserBase)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.authenticate_user(db=db, user=user)