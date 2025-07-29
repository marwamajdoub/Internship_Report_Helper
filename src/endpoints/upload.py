from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

from src.utilities.text_utils import extract_text_from_file, chunk_text, save_chunks_to_json

router = APIRouter()

# Directory to store uploaded files
UPLOAD_DIR = "src/data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file (PDF, TXT, etc.), extract and chunk its text content, 
    and save both the file and its chunks.

    Returns:
        - filename: original uploaded file name
        - num_chunks: number of text chunks extracted
        - chunks_saved_to: path to saved chunked JSON
        - message: upload + process status
    """
    # Path to save the file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Extract text from file
        text = extract_text_from_file(file_path)

        # Chunk the text into pieces
        chunks = chunk_text(text, chunk_size=500)

        # Save the chunks to JSON
        chunk_file_path = save_chunks_to_json(chunks, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "chunks_saved_to": chunk_file_path,
        "message": "File uploaded and processed successfully"
    }
