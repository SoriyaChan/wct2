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

admin = {"name": "soriya", "email": "soriya@gmail.com", "password": "12345"}

def check_user_login(db: Session, request: Request):
    username = request.cookies.get("username")

    if username == admin["name"]:
        return username
    
    if not username:
        raise HTTPException(status_code=401, detail="Log in First!")
    
    existing_user = db.query(User).filter(User.userName == username).first()
    
    return existing_user.userName