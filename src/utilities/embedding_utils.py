import os
import json
from src.embeddings.sparse_embedder import SparseEmbedder

def load_chunk_texts_from_json_folder(folder_path="src/data"):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                chunks = json.load(f)
                for chunk in chunks:
                    text = chunk.get("text", "").strip()
                    if text:
                        documents.append(text)
    return documents

# Load all chunk texts from JSON files in src/data
documents_texts = load_chunk_texts_from_json_folder()

# Initialize SparseEmbedder and fit on all documents (chunks)
sparse_model = SparseEmbedder()
sparse_model.fit_transform(documents_texts)
