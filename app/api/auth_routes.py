from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schema import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse
)
from app.services.auth_service import register_user_service, login_user_service

from app.auth.dependencies import (
    get_db_session,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Endpoint for user registration
@router.post("/register", status_code=status.HTTP_201_CREATED)

def register_user(
    request: UserRegisterRequest,
    database_session: Session = Depends(get_db_session)
):
    register_user_service(database_session, request.username, request.password)
    return {"message": "User registered successfully"}

# Endpoint for user login
@router.post("/login")
def login_user(
    # request: UserLoginRequest,
    form_data: OAuth2PasswordRequestForm = Depends(),
    database_session: Session = Depends(get_db_session)
):
    token = login_user_service(database_session, form_data.username, form_data.password)
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Protected endpoint to test authentication
@router.get("/me")
def get_profile(
    current_user = Depends(get_current_user)
):
    return {"username": current_user.username}
