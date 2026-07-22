import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate

# ==========================================
# Load Environment
# ==========================================

import streamlit as st

load_dotenv()

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

# ==========================================
# LLM
# ==========================================

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# ==========================================
# Embedding Model
# ==========================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# Load Vector Database
# ==========================================

vectorstore = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k":3}
)

# ==========================================
# Prompt
# ==========================================

rag_prompt = ChatPromptTemplate.from_template("""
Anda adalah AI Assistant pada perusahaan HR Recruitment.

Jawablah pertanyaan HANYA berdasarkan dokumen perusahaan.

Jika informasi tidak tersedia, jawab:

"Maaf, informasi tersebut tidak terdapat pada knowledge base perusahaan."

Context:
{context}

Question:
{question}

Jawaban:
""")

# ==========================================
# Retrieve Context
# ==========================================

def retrieve_context(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context, docs

# ==========================================
# RAG Answer
# ==========================================

def rag_answer(question):

    context, docs = retrieve_context(question)

    prompt = rag_prompt.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "documents": docs
    }
