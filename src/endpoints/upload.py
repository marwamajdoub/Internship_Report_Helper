# src/endpoints/upload.py

from fastapi import APIRouter, UploadFile, File
import os
import shutil

# Create a new APIRouter instance to handle file upload endpoints
router = APIRouter()

# Define the directory where uploaded files will be stored
UPLOAD_DIR = "src/data"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True) 

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a single file (PDF, TXT, etc.) to the server.

    - Saves the uploaded file to the `src/data/` directory.
    - Returns the filename and a success message.

    Args:
        file (UploadFile): File uploaded through the API.

    Returns:
        dict: Filename and success message.
    """
    # Build the full file path
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file using a binary write operation
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully"
    }
