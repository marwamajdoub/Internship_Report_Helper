import faiss
import numpy as np
import os

FAISS_INDEX_PATH = "src/data/dense.index" 

class FaissIndex:
    def __init__(self, dim):
        self.dim = dim
        self.index = None
        self.load_or_initialize()

    def load_or_initialize(self):
        if os.path.exists(FAISS_INDEX_PATH):
            print("Loading existing FAISS index...")
            self.index = faiss.read_index(FAISS_INDEX_PATH)
        else:
            print("Creating new FAISS index...")
            self.index = faiss.IndexFlatL2(self.dim)

    def add(self, vectors):
        print(f"Adding {len(vectors)} vectors to FAISS index")
        self.index.add(np.array(vectors).astype('float32'))
        faiss.write_index(self.index, FAISS_INDEX_PATH)

    def search(self, query_vector, top_k=5):
        if self.index.ntotal == 0:
            print("Warning: FAISS index is empty.")
            return [], []
        distances, indices = self.index.search(np.array([query_vector]).astype('float32'), top_k)
        return distances, indices
