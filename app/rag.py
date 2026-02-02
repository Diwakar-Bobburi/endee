import os
from google import genai
from retriever import retrieve_top_k

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def build_prompt(question, retrieved_chunks):
    context = "\n\n".join(
        [f"- {meta['text']}" for _, meta in retrieved_chunks]
    )

    return f"""
You are an intelligent assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""


def generate_answer(question):
    print("🔎 Retrieving relevant context...")
    retrieved = retrieve_top_k(question, k=3)

    prompt = build_prompt(question, retrieved)

    try:
        print("🧠 Generating answer with Gemini...")
        response = client.models.generate_content(
            model="gemini-1.0-pro",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print("⚠️ Gemini model unavailable, returning context-based answer")
        return "\n\n".join(
            [meta["text"] for _, meta in retrieved]
        )



if __name__ == "__main__":
    q = input("Ask a question: ")
    answer = generate_answer(q)
    print("\n💡 Answer:\n")
    print(answer)
