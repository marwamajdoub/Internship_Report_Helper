import json
from sentence_transformers import SentenceTransformer
from src.embeddings.faiss_index import FaissIndex  # your FAISS wrapper class

# Step 1: Load your chunked data (each chunk is a text string)
with open("src/data/chunks/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# Step 2: Initialize the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
DIMENSION = 384

# Step 3: Embed all chunks at once (returns a numpy array of shape (num_chunks, 384))
vectors = model.encode(chunks, convert_to_numpy=True)

print(f"Encoded vectors shape: {vectors.shape}")

# Step 4: Initialize or load your FAISS index wrapper
index = FaissIndex(dim=DIMENSION)

# Step 5: Add vectors to the FAISS index and save to disk inside add() method
index.add(vectors)

print("FAISS index built and saved.")
