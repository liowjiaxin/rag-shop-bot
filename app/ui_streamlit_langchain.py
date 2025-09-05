import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from rag
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.langchain_rag import LangChainRAG

st.set_page_config(page_title="Shop RAG Bot (LangChain)", layout="centered")
st.title("🛍️ Shop RAG Chatbot (LangChain Edition)")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

if "rag_system" not in st.session_state:
    with st.spinner("Loading RAG system..."):
        try:
            st.session_state.rag_system = LangChainRAG()
            st.success("✅ LangChain RAG system loaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading RAG system: {e}")
            st.stop()

# Chat input
query = st.chat_input("Ask about products, shipping, returns...")

if query:
    # Add user message to history
    st.session_state.history.append(("user", query))
    
    # Get response from LangChain RAG
    with st.spinner("Thinking..."):
        try:
            answer = st.session_state.rag_system.query(query)
            st.session_state.history.append(("assistant", answer))
        except Exception as e:
            error_msg = f"⚠️ Error: {e}"
            st.session_state.history.append(("assistant", error_msg))

# Display chat history
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg)

# Sidebar with information
with st.sidebar:
    st.header("🔍 System Info")
    st.write("**Framework:** LangChain")
    st.write("**LLM:** Groq (llama-3.1-8b-instant)")
    st.write("**Vector DB:** FAISS")
    st.write("**Embeddings:** sentence-transformers")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.history = []
        st.rerun()
    
    # Debug section
    if st.checkbox("🐛 Debug Mode"):
        if query:
            st.subheader("Retrieved Documents")
            try:
                docs = st.session_state.rag_system.get_relevant_docs(query)
                for i, doc in enumerate(docs, 1):
                    with st.expander(f"Document {i} (Score: {doc.metadata.get('score', 'N/A')})"):
                        st.write(f"**Source:** {doc.metadata.get('source', 'Unknown')}")
                        st.write(f"**Title:** {doc.metadata.get('title', 'Unknown')}")
                        st.write(f"**Content:** {doc.page_content[:200]}...")
            except Exception as e:
                st.error(f"Debug error: {e}")
