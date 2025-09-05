import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# Load environment variables
load_dotenv()

class CustomEmbeddings(Embeddings):
    """Custom embeddings wrapper that uses SentenceTransformer directly"""
    
    def __init__(self, model):
        self.model = model
    
    def embed_documents(self, texts):
        """Embed a list of documents"""
        embeddings = self.model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
    
    def embed_query(self, text):
        """Embed a single query"""
        embedding = self.model.encode([text], normalize_embeddings=True)
        return embedding[0].tolist()

class LangChainRAG:
    def __init__(self, index_path="data/faiss.index", meta_path="data/meta.jsonl", top_k=5):
        self.top_k = top_k
        
        # Initialize LLM
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.2
        )
        
        # Initialize embeddings using the same approach as the working custom implementation
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.embeddings = CustomEmbeddings(self.embedding_model)
        
        # Load FAISS index and metadata
        self._load_vectorstore(index_path, meta_path)
        
        # Create RAG chain
        self._create_rag_chain()
    
    def _load_vectorstore(self, index_path, meta_path):
        """Load existing FAISS index and metadata into LangChain format"""
        # Load metadata
        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = [json.loads(line) for line in f]
        
        # Create documents from metadata
        documents = []
        for meta in metadata:
            doc = Document(
                page_content=meta["text"],
                metadata={
                    "source": meta["source"],
                    "id": meta["id"],
                    "title": meta.get("title", "")
                }
            )
            documents.append(doc)
        
        # Create vectorstore from documents (this will create embeddings and index)
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
    
    def _create_rag_chain(self):
        """Create the LangChain RAG chain"""
        # Create prompt template
        prompt_template = """You are a helpful e-commerce assistant.
Use ONLY the context below to answer the question.
If the context is not enough, say you don't know.

Question: {question}

Context:
{context}

Answer:"""
        
        self.prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.top_k}
        )
        
        # Create RAG chain
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        self.rag_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def query(self, question: str) -> str:
        """Query the RAG system with LangChain"""
        try:
            response = self.rag_chain.invoke(question)
            return response
        except Exception as e:
            return f"⚠️ Error processing query: {e}"
    
    def get_relevant_docs(self, question: str):
        """Get relevant documents for debugging/inspection"""
        return self.retriever.get_relevant_documents(question)

# For backward compatibility with existing code
def create_langchain_rag():
    """Factory function to create LangChain RAG instance"""
    return LangChainRAG()
