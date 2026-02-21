from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db_session
from app.auth.authorization import require_permission
from app.services.admin_services import assign_role_to_user_service, list_users_with_roles_service

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/assign-role", status_code=status.HTTP_200_OK)
def assign_role_to_user(
    username: str,
    role_name: str,
    db: Session = Depends(get_db_session),
    # current_user = Depends(require_permission("assign_role"))
):
    return assign_role_to_user_service(db, username, role_name)

@router.get("/users")
def list_users(
    db: Session = Depends(get_db_session),
    # current_user = Depends(require_permission("list_users"))
):
    return list_users_with_roles_service(db)
