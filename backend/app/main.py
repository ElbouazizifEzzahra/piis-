from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs when the server starts
    create_db_and_tables()
    yield
    # Anything after 'yield' runs when the server shuts down

app = FastAPI(title="PIIS Backend API", lifespan=lifespan)

# CORS (Allow Frontend to talk to Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], #   Vite port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event: Create Database Tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include API Router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to  PIIS Backend"}