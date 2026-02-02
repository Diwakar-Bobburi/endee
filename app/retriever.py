import json
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "data/endee_vectors.json"


def load_vector_store():
    """
    Load stored vectors from Endee-style JSON store
    """
    with open(VECTOR_STORE_PATH, "r") as f:
        return json.load(f)


def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def retrieve_top_k(query: str, k: int = 5):
    """
    Retrieve top-k most similar chunks for a query
    """
    print("🔍 Embedding user query...")
    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode(query)

    print("📦 Loading vector store...")
    records = load_vector_store()

    similarities = []

    for record in records:
        score = cosine_similarity(query_embedding, record["vector"])
        similarities.append((score, record["metadata"]))

    # Sort by similarity score (descending)
    similarities.sort(key=lambda x: x[0], reverse=True)

    return similarities[:k]


if __name__ == "__main__":
    query = input("Enter your question: ")
    results = retrieve_top_k(query, k=3)

    print("\n🔝 Top relevant chunks:\n")
    for idx, (score, meta) in enumerate(results, 1):
        print(f"{idx}. Score: {score:.4f}")
        print(f"   Source: {meta['source']}")
        print(f"   Text: {meta['text'][:300]}...\n")
