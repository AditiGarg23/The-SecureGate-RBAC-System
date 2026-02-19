from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth.jwt_handler import verify_access_token
from app.models import user
from app.repositories.user_repo import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency to get DB session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user from token
def get_current_user(
    token: str = Depends(oauth2_scheme), 
    database_session: Session = Depends(get_db_session)
):
    
    payload = verify_access_token(token)
    username = payload.get("sub")

    user = get_user_by_username(database_session, username)

    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
