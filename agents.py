from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag import rag_answer, llm

# ==========================================
# Output Parser
# ==========================================

output_parser = StrOutputParser()

# ==========================================
# Base Agent
# ==========================================

def run_agent(role: str, question: str):
    """
    Menjalankan agent berdasarkan role.
    Semua agent menggunakan RAG Tool yang sama.
    """

    rag_result = rag_answer(question)

    context = "\n\n".join(
        [doc.page_content for doc in rag_result["documents"]]
    )

    prompt = ChatPromptTemplate.from_template("""
Anda adalah {role} pada perusahaan HR Recruitment.

Tugas Anda:

- Jawab hanya berdasarkan context.
- Jangan mengarang jawaban.
- Jika informasi tidak tersedia, katakan bahwa informasi tidak ditemukan.
- Berikan jawaban yang profesional dan jelas.

Context:
{context}

Question:
{question}
""")

    chain = prompt | llm | output_parser

    answer = chain.invoke({
        "role": role,
        "context": context,
        "question": question
    })

    return {
        "agent": role,
        "answer": answer,
        "documents": rag_result["documents"]
    }

# ==========================================
# CV Screening Agent
# ==========================================

def cv_agent(question):
    return run_agent(
        "CV Screening Specialist",
        question
    )

# ==========================================
# Interview Agent
# ==========================================

def interview_agent(question):
    return run_agent(
        "Interview Coordinator",
        question
    )

# ==========================================
# Training Agent
# ==========================================

def training_agent(question):
    return run_agent(
        "Training and Onboarding Specialist",
        question
    )

# ==========================================
# Client Relations Agent
# ==========================================

def client_agent(question):
    return run_agent(
        "Client Relations Officer",
        question
    )

# ==========================================
# Reporting Agent
# ==========================================

def reporting_agent(question):
    return run_agent(
        "Reporting Analyst",
        question
    )