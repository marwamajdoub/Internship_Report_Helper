from fastapi import APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from src.embeddings.faiss_index import FaissIndex

router = APIRouter()

# Load model and index
model = SentenceTransformer("all-MiniLM-L6-v2")
DIMENSION = 384  # dimension for MiniLM model
index = FaissIndex(dim=DIMENSION)

# Pydantic model for the request
class SearchRequest(BaseModel):
    query_text: str
    top_k: int = 5

@router.post("/")
def search_faiss(data: SearchRequest):
    # Convert query text into dense vector
    query_vector = model.encode(data.query_text)

    # Perform FAISS search
    distances, indices = index.search(query_vector, data.top_k)

    return {
        "query": data.query_text,
        "distances": distances,
        "indices": indices
    }

