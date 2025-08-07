# main.py

from fastapi import FastAPI
from src.endpoints import upload
from src.endpoints import search
from src.endpoints import health_check

app = FastAPI(title="Internship Report Helper")

# Include the upload endpoint
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(search.router, prefix="/search")
app.include_router(health_check.router)
   
@app.get("/")
def read_root():
    return {"message": "Welcome to Internship Report Helper!"}
