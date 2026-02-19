from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.role import Role
from app.repositories.user_repo import get_user_by_username, create_user
from app.auth.hashing import verify_password, hash_password
from app.auth.jwt_handler import create_access_token

#Service function for user registration
def register_user_service(database_session: Session, username:str, password: str):
    existing_user = get_user_by_username(database_session, username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    hashed_password = hash_password(password)

    new_user = create_user(database_session, username, hashed_password)

    user_role = database_session.query(Role).filter(Role.name == "User").first()

    if not user_role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Default User role not found"
        )

    # 🔥 Assign role
    new_user.roles.append(user_role)

    database_session.commit()
    database_session.refresh(new_user)

    return new_user

# Service function for user login
def login_user_service(database_session: Session, username: str, password: str):
    user = get_user_by_username(database_session, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return access_token