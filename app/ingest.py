import os
from pypdf import PdfReader

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def load_documents(directory: str):
    """
    Load PDF and TXT documents from a directory
    """
    documents = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if filename.endswith(".pdf"):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            documents.append({
                "text": text,
                "source": filename
            })

        elif filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "text": text,
                "source": filename
            })

    return documents


def chunk_text(text: str):
    """
    Split text into overlapping chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def ingest_documents(directory: str):
    """
    Load documents and convert them into chunks
    """
    documents = load_documents(directory)
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "chunk_id": i,
                "text": chunk,
                "source": doc["source"]
            })

    return all_chunks


if __name__ == "__main__":
    docs_path = "data/documents"
    chunks = ingest_documents(docs_path)
    print(f"Total chunks created: {len(chunks)}")
