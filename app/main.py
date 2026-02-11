from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine,Base

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield # app runs here
    # Cleanup code (if needed) goes here

    # Code that runs on shutdown
    print("App Shutting down...")

app = FastAPI(lifespan=lifespan)
