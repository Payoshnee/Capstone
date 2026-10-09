from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.schemas.common import APIResponse, APIError
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import user_service
from app.core.security import create_access_token, verify_password, verify_token
from fastapi import HTTPException
from app.models.user import User

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user: UserResponse

class BootstrapResponse(BaseModel):
    id: str
    email: str
    role: str
    expert_approval_required: bool

@router.post("/bootstrap", response_model=APIResponse[BootstrapResponse])
async def bootstrap_user(
    claims: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.bootstrap_auth_user(db, claims)
    return APIResponse(data=BootstrapResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        expert_approval_required=user.role == "expert",
    ))

@router.post("/signup", response_model=APIResponse[UserResponse])
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.create_user(db, user_in)
        return APIResponse(data=UserResponse(id=user.id, email=user.email, full_name=user.full_name, role=user.role))
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))

@router.post("/login", response_model=APIResponse[AuthResponse])
async def login(login_in: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.get_by_email(db, login_in.email.lower().strip())
        if not user or not verify_password(login_in.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        user_resp = UserResponse(id=user.id, email=user.email, full_name=user.full_name, role=user.role)
        
        return APIResponse(data=AuthResponse(
            token=create_access_token(user.id, user.email),
            user=user_resp
        ))
    except HTTPException:
        raise
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))

@router.get("/me", response_model=APIResponse[UserResponse])
async def get_me(claims: dict = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    user = await db.get(User, claims["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(data=UserResponse(
        id=user.id, email=user.email, full_name=user.full_name, role=user.role
    ))
