from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email_institucional: EmailStr
    nome_completo: str

class UserCreate(UserBase):
    senha: str = Field(..., min_length=6)
    matricula: Optional[str] = None

class UserLogin(BaseModel):
    email_institucional: EmailStr
    senha: str

class UserProfile(UserBase):
    id: str
    matricula: Optional[str]
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserProfile
