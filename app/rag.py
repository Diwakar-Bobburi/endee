import os
import google.genai as genai
from app.retriever import retrieve_top_k


def generate_answer(query):
    # Step 1: Retrieve context
    context = retrieve_top_k(query)

    if not context:
        return "No relevant context found."

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""

    # Step 2: Check API key
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "[LLM disabled – GEMINI_API_KEY not set]\n\n"
            "Retrieved context:\n"
            f"{context}"
        )

    # Step 3: Call Gemini safely
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text

    except Exception:
        return (
            "[LLM error – fallback to retrieved context]\n\n"
            f"{context}"
        )
