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
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Extract text
        text = extract_text_from_file(file_path)

        # Chunk the text
        chunks = chunk_text(text, chunk_size=500)

        # Save the chunks
        chunk_file_path = save_chunks_to_json(chunks, file.filename)

        # ---- NEW: Embedding and Indexing ----
        from src.embeddings.dense_embedder import DenseEmbedder
        from src.embeddings.faiss_index import FaissIndex

        embedder = DenseEmbedder()
        DIMENSION = 384  # adjust if needed
        faiss_index = FaissIndex(dim=DIMENSION)

        embeddings = embedder.encode(chunks)
        faiss_index.add(embeddings)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "num_chunks": len(chunks),
        "chunks_saved_to": chunk_file_path,
        "message": "File uploaded, processed, and indexed successfully"
    }
