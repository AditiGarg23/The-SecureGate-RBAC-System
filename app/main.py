from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine,Base
from app.utils.seed import seed_data
from app.api import api_router, protected_router

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine) # Created tables
    seed_data()  # Seed initial data

    yield # app runs here
    
    # Code that runs on shutdown
    print("App Shutting down...")


app = FastAPI(title= "SecureGate RBAC", lifespan=lifespan)

app.include_router(api_router)
app.include_router(protected_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}






