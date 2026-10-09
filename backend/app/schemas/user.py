from pydantic import BaseModel
from typing import Literal, Optional

class UserCreate(BaseModel):
    email: str
    full_name: Optional[str] = None
    password: str
    role: Literal["candidate", "expert"] = "candidate"

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    role: str = "candidate"

class ProfileUpdate(BaseModel):
    target_role: Optional[str] = None
    bio: Optional[str] = None
