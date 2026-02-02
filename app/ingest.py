import os
import json
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# ---------------- CONFIG ---------------- #

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MODEL_NAME = "all-MiniLM-L6-v2"

DOCUMENTS_PATH = "data/documents"
VECTOR_STORE_PATH = "data/endee_vectors.json"

# ---------------------------------------- #


def load_documents(directory):
    """
    Load PDF and TXT documents from a directory
    """
    documents = []

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)

        if filename.endswith(".pdf"):
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            documents.append((filename, text))

        elif filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                documents.append((filename, f.read()))

    return documents


def chunk_text(text):
    """
    Split text into overlapping chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def load_vector_store():
    """
    Load existing vector store or create a new one
    """
    if os.path.exists(VECTOR_STORE_PATH):
        with open(VECTOR_STORE_PATH, "r") as f:
            return json.load(f)
    return []


def save_vector_store(data):
    """
    Save vectors to local Endee-style store
    """
    with open(VECTOR_STORE_PATH, "w") as f:
        json.dump(data, f, indent=2)


def ingest_documents():
    """
    Full ingestion pipeline:
    documents -> chunks -> embeddings -> vector store
    """
    print("🔹 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("🔹 Loading documents...")
    documents = load_documents(DOCUMENTS_PATH)

    if not documents:
        print("⚠️ No documents found.")
        return

    vector_store = load_vector_store()
    total_chunks = 0

    for filename, text in documents:
        chunks = chunk_text(text)
        embeddings = model.encode(chunks)

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            record = {
                "vector": embedding.tolist(),
                "metadata": {
                    "text": chunk,
                    "source": filename,
                    "chunk_id": i
                }
            }
            vector_store.append(record)
            total_chunks += 1

    save_vector_store(vector_store)

    print(f"✅ Ingestion complete!")
    print(f"📦 Total chunks stored: {total_chunks}")
    print(f"💾 Vector store saved at: {VECTOR_STORE_PATH}")


if __name__ == "__main__":
    ingest_documents()
