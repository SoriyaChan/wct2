from sqlalchemy.orm import Session
from ..models import User 
from app.schemas import user as schemas
from ..dependency import admin
from fastapi import HTTPException, Response
import hashlib


def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(User).filter(
        (User.userName == user.userName) | (User.userEmail == user.userEmail)).first()

    if existing_user or user.userName == admin["name"]:
        raise HTTPException(
            status_code=409,
            detail="A user with this username or email already exists."
        )
    
    hash_password = hashlib.sha512(user.password.encode())

    db_user = User(userName=user.userName, userEmail=user.userEmail, password=hash_password.hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, user: schemas.UserLogin, response: Response):
    if user.userEmail == admin["email"] and user.password == admin["password"]:
        response.set_cookie(key="username", value=admin["name"])
        return {"message": f"Welcome admin, {admin['name']}!"}

    existing_user = db.query(User).filter(User.userEmail == user.userEmail).first()

    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found",
        )
    
    hash_password = hashlib.sha512(user.password.encode())

    if existing_user.password != hash_password.hexdigest():
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    response.set_cookie(key="username", value=existing_user.userName)
    return {"message": f"Welcome, {existing_user.userName}!"}
