from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import engine, Base
import os

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pest Detection API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow all. In prod, specify Vue app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Welcome to Pest Detection API"}

from backend.routers import auth, detection, forum, users, admin

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(detection.router)
app.include_router(forum.router)
app.include_router(admin.router)

