# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    # Replaced 'username' with 'identifier' so the frontend can send either CIN or TEL
    identifier: str 
    password: str

class UserCreate(BaseModel):
    # Fields perfectly aligned with  UML
    cin: str
    tel: Optional[str] = None
    email: Optional[str] = None
    full_name: str
    password: str