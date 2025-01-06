from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    userName: str
    userEmail: EmailStr 
    role: str

class UserCreate(UserBase):
    password: str
    api_key: Optional[str] = None

class UserLogin(BaseModel):
    userEmail: EmailStr
    password: str

class User(UserBase):
    userID: int
    api_key: str
    password: str

    class Config:
        from_attributes = True