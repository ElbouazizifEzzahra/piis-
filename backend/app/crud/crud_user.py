from sqlmodel import Session, select, or_
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_identifier(session: Session, identifier: str) -> User | None:
    """
    Auth v2.3: Fetches a user by checking if the identifier matches 
    either their CIN or their Telephone number.
    """
    # or_ allows us to check multiple conditions in the WHERE clause
    statement = select(User).where(
        or_(
            User.cin == identifier, 
            User.tel == identifier
        )
    )
    return session.exec(statement).first()

def get_user_by_cin(session: Session, cin: str) -> User | None:
    """Useful for registration to ensure a CIN isn't already taken."""
    statement = select(User).where(User.cin == cin)
    return session.exec(statement).first()

def create_user(session: Session, user_create: UserCreate) -> User:
    """Hashes the password and saves a new user with all required UML fields."""
    db_user = User(
        cin=user_create.cin,
        tel=user_create.tel,
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password) 
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user