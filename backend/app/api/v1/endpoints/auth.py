from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.core.security import create_access_token, verify_password
from app.schemas.user import UserLogin, UserCreate
from app.schemas.token import Token

from app.crud import crud_user 

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(form_data: UserLogin, session: Session = Depends(get_session)) -> Any:
    # 1. Auth v2.3: Check user by CIN or TEL (we'll call it 'identifier' in the schema)
    user = crud_user.get_user_by_identifier(session=session, identifier=form_data.identifier)
    
    # 2. Check Password 
    if not user or not verify_password(form_data.password, user.hashed_password):
        # Updated error message to be more precise but still secure
        raise HTTPException(status_code=400, detail="Incorrect CIN/TEL or password")
    
    # 3. Generate Token
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }

@router.post("/register", response_model=Token)
def register_user(user_in: UserCreate, session: Session = Depends(get_session)) -> Any:
    # 1a. Check if the mandatory CIN already exists
    existing_user_cin = crud_user.get_user_by_cin(session=session, cin=user_in.cin)
    if existing_user_cin:
        raise HTTPException(status_code=400, detail="A user with this CIN is already registered")
        
    # 1b. Check if the optional TEL is provided and already taken
    if user_in.tel:
        existing_user_tel = crud_user.get_user_by_identifier(session=session, identifier=user_in.tel)
        if existing_user_tel:
            raise HTTPException(status_code=400, detail="A user with this phone number is already registered")
    
    # 2. Delegate to CRUD to Create User
    user = crud_user.create_user(session=session, user_create=user_in)
    
    # 3. Return Token immediately
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }