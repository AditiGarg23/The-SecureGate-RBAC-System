from fastapi import APIRouter
from app.api.auth_routes import router as auth_router
from app.api.protected_routes import router as protect_router

api_router = APIRouter()
protected_router = APIRouter()
api_router.include_router(auth_router)
protected_router.include_router(protect_router)
