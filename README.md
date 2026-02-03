# RAG-Based Document Question Answering using Endee

This project implements a **Retrieval-Augmented Generation (RAG)** based Document Question Answering system using **Endee** as the vector database foundation.

The system allows users to ask natural language questions over their documents and receive context-aware answers using semantic search and a large language model.

---

## 🚀 Features

- Document ingestion (PDF / TXT)
- Text chunking with overlap
- Embedding generation using SentenceTransformers
- Vector-based semantic search (Endee-style vector store)
- RAG pipeline with context grounding
- LLM-based answer generation (Gemini with graceful fallback)
- Clean, modular, and evaluation-ready codebase

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** combines:
- **Retrieval**: Fetching relevant document chunks using vector similarity
- **Generation**: Using an LLM to generate answers grounded in retrieved context

This reduces hallucinations and improves factual accuracy.

---

## 🗄️ Role of Endee (Vector Database)

Endee is designed as a high-performance native vector database.

In this project:
- The Endee repository is forked and used as the base
- Vector embeddings follow Endee’s vector storage design
- Vectors and metadata are persisted in an Endee-compatible format
- Semantic similarity search is the core retrieval mechanism

> Due to platform constraints on Windows, the project demonstrates Endee integration using its vector schema and retrieval logic, while maintaining the same architecture that can be deployed with the Endee service in production environments.

---

## 🏗️ Project Architecture

Documents (PDF/TXT)
↓
Text Chunking
↓
Embedding Generation (SentenceTransformers)
↓
Vector Store (Endee-style)
↓
Semantic Search (Cosine Similarity)
↓
Relevant Context
↓
LLM (Gemini) → Final Answer


---

## 📂 Project Structure

endee/
│
├── app/
│ ├── ingest.py # Document ingestion & embedding
│ ├── retriever.py # Semantic search logic
│ ├── rag.py # RAG pipeline (retrieval + generation)
│ └── main.py # Application entry point
│
├── data/
│ ├── documents/ # Input documents
│ └── endee_vectors.json
│
├── requirements.txt
└── README.md


---

## 🛠️ Tech Stack

- Python
- SentenceTransformers (`all-MiniLM-L6-v2`)
- NumPy
- Google Gemini (LLM)
- Endee (vector database foundation)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/endee.git
cd endee


2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Add Documents

Place your PDF or TXT files inside:

data/documents/

▶️ Running the Project
Step 1: Ingest Documents
python app/ingest.py


This will:

Load documents

Generate embeddings

Store vectors in an Endee-compatible format

Step 2: Ask Questions (RAG)
python -m app.main


Example:

Ask a question: What is artificial intelligence?

🤖 LLM Configuration (Optional)

The project supports Google Gemini for answer generation.

Set the API key:

set GEMINI_API_KEY=your_api_key_here


If the `GEMINI_API_KEY` environment variable is not set, the system will safely fall back to returning answers based on retrieved document context.