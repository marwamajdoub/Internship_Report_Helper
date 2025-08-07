from fastapi import APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from src.embeddings.faiss_index import FaissIndex
from src.utilities.llm_response import generate_answer  # <- you create this file below
import json

router = APIRouter()

# Load embedding model and index
model = SentenceTransformer("all-MiniLM-L6-v2")
DIMENSION = 384
index = FaissIndex(dim=DIMENSION)

# Load all chunks once at startup
with open("src/data/chunks/chunks.json", "r", encoding="utf-8") as f:
    all_chunks = json.load(f)

# Request body model
class SearchRequest(BaseModel):
    query_text: str
    top_k: int = 5

@router.post("/")
def search_faiss(data: SearchRequest):
    # Step 1: Convert query into dense vector
    query_vector = model.encode(data.query_text)

    # Step 2: Search top_k chunks using FAISS
    distances, indices = index.search(query_vector, data.top_k)

    # Step 3: Retrieve top_k chunk texts
    top_chunks = [all_chunks[i] for i in indices[0]]

    # Step 4: Generate answer from LLM using retrieved chunks
    answer = generate_answer(data.query_text, top_chunks)

    # Step 5: Return full response
    return {
        "query": data.query_text,
        "answer": answer,
        "retrieved_chunks": top_chunks,
        "distances": distances.tolist(),
        "indices": indices.tolist()
    }
