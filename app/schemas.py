from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    name: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ChatQuery(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

class DocumentUploadResponse(BaseModel):
    status: str
    message: str
    chunks: int