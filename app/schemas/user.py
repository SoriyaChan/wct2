from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    userName: str
    userEmail: EmailStr 
    role: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    userEmail: EmailStr
    password: str

class User(UserBase):
    userID: int
    password: str

    class Config:
        from_attributes = True