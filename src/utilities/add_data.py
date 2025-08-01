import json
from sentence_transformers import SentenceTransformer
from src.embeddings.faiss_index import FaissIndex

# Load chunks
with open("src/data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Embed chunks
model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(chunks)

print(f"Encoded vectors shape: {vectors.shape}")

# Create index and add vectors
DIMENSION = 384
index = FaissIndex(dim=DIMENSION)
index.add(vectors)  # This writes the index to disk

print("FAISS index built and saved.")
