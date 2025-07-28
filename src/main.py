# main.py

from fastapi import FastAPI
from src.endpoints import upload

app = FastAPI(title="Internship Report Helper")

# Include the upload endpoint
app.include_router(upload.router, prefix="/upload", tags=["Upload"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Internship Report Helper!"}
