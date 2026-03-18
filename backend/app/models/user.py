import uuid
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

# 1. Define the Enum from the UML
class AccountStatus(str, Enum):
    Active = "Active"
    Archived = "Archived"
    Suspended = "Suspended"

# 2. Base model for shared properties
class UserBase(SQLModel):
    cin: str = Field(unique=True, index=True, description="Identifiant auth principal (Loi 09-08)")
    tel: Optional[str] = Field(default=None, unique=True, description="Identifiant auth alternatif")
    email: Optional[str] = Field(default=None, unique=True)
    full_name: str
    account_status: AccountStatus = Field(default=AccountStatus.Active)

# 3. Database Table Model
class User(UserBase, table=True):
    # UUID Primary Key as defined in UML
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # Keeping it as 'hashed_password' instead of 'password' for security best practices
    hashed_password: str 
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = Field(default=None)

    # Relationships (Ready for when you create the other models)
    # reports: List["Report"] = Relationship(back_populates="user")
    # roles: List["UserRoleAssignment"] = Relationship(back_populates="user")