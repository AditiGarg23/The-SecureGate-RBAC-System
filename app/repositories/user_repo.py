from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_username(database_session: Session, username: str):
    return database_session.query(User).filter(User.username == username).first()

def create_user(database_session: Session, username: str, hashed_password: str):
    new_user = User(username=username, password=hashed_password)

    database_session.add(new_user)
    database_session.commit()
    database_session.refresh(new_user)
    return new_user