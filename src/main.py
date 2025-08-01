# main.py

from fastapi import FastAPI
from src.endpoints import upload
from src.endpoints import search


app = FastAPI(title="Internship Report Helper")

# Include the upload endpoint
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(search.router, prefix="/search")

@app.get("/")
def read_root():
    return {"message": "Welcome to Internship Report Helper!"}
