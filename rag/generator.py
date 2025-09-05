import os
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_answer(question, hits):
    """
    Generate an answer using Groq-hosted LLaMA-3.
    """
    if not hits:
        return "Sorry, I don’t have an answer for that."

    # Combine retrieved chunks
    context = "\n\n".join([doc["text"] for doc, _ in hits])

    prompt = f"""
    You are a helpful e-commerce assistant.
    Use ONLY the context below to answer the question.
    If the context is not enough, say you don't know.

    Question: {question}
    Context:
    {context}

    Answer:
    """

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {
        "model": "llama-3.1-8b-instant",   # current Groq-hosted modeladd docs: add comprehensive README with project overview, features, setup instructions, and tech stack

        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Error contacting Groq API: {e}"
