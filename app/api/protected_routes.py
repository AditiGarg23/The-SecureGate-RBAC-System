from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.authorization import require_permission

router = APIRouter(
    prefix="/test",
    tags=["Test"]
)

@router.get("/read")
def read_protected_data(permission: str = Depends(require_permission("READ_DATA"))):
    return {"message": "You have access to read protected data!"}

@router.post("/delete")
def delete_protected_data(permission: str = Depends(require_permission("DELETE_DATA"))):
    return {"message": "You have access to delete protected data!"}
