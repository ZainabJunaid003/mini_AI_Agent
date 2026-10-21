import os
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # free, runs locally
chunks, vectors = [], None

def chunk_text(text, size=500, overlap=50):
    return [text[i:i+size] for i in range(0, len(text), size - overlap)]

def load_docs(folder="docs"):
    global chunks, vectors
    chunks = []
    for f in os.listdir(folder):
        if f.endswith(".txt"):
            with open(os.path.join(folder, f), encoding="utf-8") as fh:
                chunks += chunk_text(fh.read())
    vectors = model.encode(chunks, normalize_embeddings=True)

def search(query, k=3):
    q = model.encode([query], normalize_embeddings=True)[0]
    scores = vectors @ q          # cosine similarity (vectors are normalized)
    top = np.argsort(scores)[::-1][:k]
    return "\n---\n".join(chunks[i] for i in top)