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

# admin
admin = {"name": "soriya", "email": "soriya@gmail.com", "password": "12345"}

def check_user_login(db: Session, request: Request):
    # get cookie
    username = request.cookies.get("username")
    # if equal admins name
    if username == admin["name"]:
        return username
    # if none
    if not username:
        raise HTTPException(status_code=401, detail="Log in First!")
    # query user
    existing_user = db.query(User).filter(User.userName == username).first()
    # return name
    return existing_user.userName