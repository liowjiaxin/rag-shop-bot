import streamlit as st
from rag.retriever import Retriever
from rag.generator import generate_answer

st.set_page_config(page_title="Shop RAG Bot", layout="centered")
st.title("🛍️ Shop RAG Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

retriever = Retriever()

query = st.chat_input("Ask about products, shipping, returns...")
if query:
    hits = retriever.search(query)
    answer = generate_answer(query, hits)
    st.session_state.history.append(("user", query))
    st.session_state.history.append(("assistant", answer))

for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)
