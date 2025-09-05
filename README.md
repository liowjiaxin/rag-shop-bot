# 🛍 RAG Shop Bot

A web-based Retrieval-Augmented Generation (RAG) chatbot for e-commerce FAQs and product info. It uses **Groq API** hosting LLaMA-3 models for generating natural and concise answers.

---

##  Features

- Uses vector retrieval (from product catalog and FAQs) with **FAISS**
- Generates LLM-powered responses using **Groq API** (free tier)
- Interactive **Streamlit** chat interface
- Safe architecture: Secrets stored in `.env`, Git-friendly `.gitignore`

---

##  Tech Stack

- Python, Streamlit (UI)
- FAISS (vector database)
- Groq API (LLM inference)
- `python-dotenv` (secure keys via `.env`)

---

##  Getting Started

1. Clone the repo:
    ```bash
    git clone https://github.com/liowjiaxin/rag-shop-bot.git
    cd rag-shop-bot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file (in repo root):
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```

4. Run the chatbot:
    ```bash
    python -m streamlit run app/ui_streamlit.py
    ```

---

##  Example Queries

| Question                  | Expected Response                          |
|---------------------------|---------------------------------------------|
| “What is the return policy?” | “You can return your item within 14 days.” |
| “Tell me about Wireless Headphones” | Natural product description.

---

##  Why It Matters

This project demonstrates how to combine:
- **Retrieval-based grounding** (via FAISS embeddings)
- **Modern generative capabilities** (via Groq LLaMA-3 API)
- **Production-ready structure** (secure secrets, modular code)
- A polished UI for real-world demo

---

##  What's Next

- Product similarity via product image embeddings
- Multilingual queries (English, Malay, Chinese)
- Streaming responses (token-by-token)
- Lightweight reranking or caching for faster response

---