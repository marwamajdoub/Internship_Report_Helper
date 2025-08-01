# ----------------------
# src/embeddings/sparse_embedder.py
# ----------------------
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

VECTORIZER_PATH = "src/embeddings/vectorizer.pkl"

class SparseEmbedder:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, texts):
        vectors = self.vectorizer.fit_transform(texts)
        with open(VECTORIZER_PATH, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        return vectors

    def transform(self, texts):
        if not os.path.exists(VECTORIZER_PATH):
            raise ValueError("Sparse vectorizer not trained. Please index documents first.")
        with open(VECTORIZER_PATH, 'rb') as f:
            self.vectorizer = pickle.load(f)
        return self.vectorizer.transform(texts)
