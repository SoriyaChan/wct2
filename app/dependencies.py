from .database import SessionLocal
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from .models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_user_login(db: Session, request: Request):
    username = request.cookies.get("username")
    
    if not username:
        raise HTTPException(status_code=401, detail="Log in First!")
    
    existing_user = db.query(User).filter(User.userName == username).first()
    
    return existing_user