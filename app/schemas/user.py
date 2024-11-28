from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    userName: str
    userEmail: EmailStr 

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    userName: str
    password: str

class User(UserBase):
    userID: int

    class Config:
        from_attributes = True