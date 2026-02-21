from fastapi import APIRouter
from app.api.auth_routes import router as auth_router
from app.api.protected_routes import router as protect_router
from app.api.admin_routes import router as admin_route

api_router = APIRouter()
api_router.include_router(auth_router)
protected_router = APIRouter()
protected_router.include_router(protect_router)
admin_router = APIRouter()
admin_router.include_router(admin_route)
