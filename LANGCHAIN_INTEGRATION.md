# LangChain Integration Guide

## Overview

RAG Shop Bot now supports both **custom RAG implementation** and **LangChain-powered RAG**. This document explains the differences and how to use both approaches.

## 🔄 Two Implementations Available

### 1. Original Custom RAG (`app/ui_streamlit.py`)
- **Direct API calls** to Groq
- **Custom FAISS integration**
- **Lightweight and fast**
- **Minimal dependencies**

### 2. LangChain RAG (`app/ui_streamlit_langchain.py`) ✨ NEW
- **LangChain framework** integration
- **Standardized RAG patterns**
- **Enhanced debugging capabilities**
- **Extensible architecture**

## 🚀 How to Run

### Original Version
```bash
python -m streamlit run app/ui_streamlit.py
```

### LangChain Version
```bash
python -m streamlit run app/ui_streamlit_langchain.py
```

## 🔍 Key Differences

| Feature | Custom RAG | LangChain RAG |
|---------|------------|---------------|
| **Framework** | Custom implementation | LangChain framework |
| **Code Structure** | Direct API calls | Chain-based architecture |
| **Prompt Management** | String templates | ChatPromptTemplate |
| **Debugging** | Basic error handling | Advanced document inspection |
| **Extensibility** | Manual implementation | LangChain ecosystem |
| **Performance** | Slightly faster | More feature-rich |

## 🛠️ LangChain Benefits

### 1. **Standardized Architecture**
```python
# LangChain RAG Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### 2. **Enhanced Debugging**
- **Document inspection** in sidebar
- **Retrieval scoring** visibility
- **Chain step visualization**

### 3. **Ecosystem Integration**
- Easy to add **memory** for conversation history
- Simple **prompt versioning** and A/B testing
- **Monitoring and observability** with LangSmith
- **Easy integration** with other LangChain tools

### 4. **Prompt Templates**
```python
prompt_template = """You are a helpful e-commerce assistant.
Use ONLY the context below to answer the question.
If the context is not enough, say you don't know.

Question: {question}
Context: {context}
Answer:"""
```

## 🔧 Technical Implementation

### LangChain Components Used

1. **ChatGroq** - Groq LLM integration
2. **FAISS** - Vector store for document retrieval
3. **SentenceTransformerEmbeddings** - Text embeddings
4. **ChatPromptTemplate** - Structured prompts
5. **RunnablePassthrough** - Chain data flow
6. **StrOutputParser** - Response formatting

### Architecture Flow

```
User Query → Retriever → Document Formatting → Prompt Template → LLM → Response Parser → User
```

## 📊 Performance Considerations

### Custom RAG
- ✅ **Faster initialization** (no LangChain overhead)
- ✅ **Lower memory usage**
- ✅ **Direct control** over all components

### LangChain RAG
- ✅ **Better error handling** and debugging
- ✅ **Standardized patterns** for maintenance
- ✅ **Future extensibility** with LangChain ecosystem
- ⚠️ **Slightly higher memory usage**

## 🎯 When to Use Which

### Use Custom RAG When:
- **Performance** is critical
- **Minimal dependencies** preferred
- **Simple use case** with no future extensions planned

### Use LangChain RAG When:
- **Rapid development** and prototyping
- **Team collaboration** with standardized patterns
- **Future features** like memory, agents, or complex chains
- **Debugging and monitoring** capabilities needed

## 🔮 Future Enhancements

With LangChain integration, you can easily add:

1. **Conversation Memory**
   ```python
   from langchain.memory import ConversationBufferMemory
   ```

2. **Multiple Retrievers**
   ```python
   from langchain.retrievers import EnsembleRetriever
   ```

3. **Custom Agents**
   ```python
   from langchain.agents import create_react_agent
   ```

4. **Monitoring**
   ```python
   from langsmith import Client
   ```

## 📝 Configuration

Both implementations use the same:
- **Environment variables** (`.env` file)
- **FAISS index** (`data/faiss.index`)
- **Metadata** (`data/meta.jsonl`)
- **Groq API** with `llama-3.1-8b-instant` model

Choose the implementation that best fits your needs!
