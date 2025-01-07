from sqlalchemy.orm import Session
from ..models import User 
from app.schemas import user as schemas
from fastapi import HTTPException
import hashlib, secrets

def create_user(db: Session, user: schemas.UserCreate):
    # query existing username and email
    existing_user = db.query(User).filter(
        (User.userName == user.userName) | (User.userEmail == user.userEmail)).first()
    # if there is, can't create
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="A user with this username or email already exists."
        )
    if user.role == "admin":
        if not user.api_key:
            raise HTTPException(
                status_code=400,
                detail="API Key is required for admin role."
            )
        valid_api_key = db.query(User).filter(User.api_key == user.api_key, User.role == 'admin').first()
        if not valid_api_key:
            raise HTTPException(
                status_code=403,
                detail="Invalid API Key for admin role."
            )

    # hash password
    hash_password = hashlib.sha512(user.password.encode())
    # add user
    db_user = User(userName=user.userName, userEmail=user.userEmail, password=hash_password.hexdigest(), role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, user: schemas.UserLogin):
    # query existing email
    existing_user = db.query(User).filter(User.userEmail == user.userEmail).first()
    # if none
    if existing_user is None:
        raise HTTPException(
            status_code=404,
            detail="user not found",
        )
    # hash encode
    hash_password = hashlib.sha512(user.password.encode())
    # if password is not the same
    if existing_user.password != hash_password.hexdigest():
        raise HTTPException(
            status_code=401,
            detail="Incorrect password",
        )
    # generate key
    api_key = secrets.token_hex(32)
    existing_user.api_key = api_key
    db.commit()
    
    return {"api_key": api_key, "user_id": existing_user.userID, "role": existing_user.role}