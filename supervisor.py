from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag import llm
from agents import (
    cv_agent,
    interview_agent,
    training_agent,
    client_agent,
    reporting_agent
)

# ==========================================
# Output Parser
# ==========================================

output_parser = StrOutputParser()

# ==========================================
# Daftar Agent
# ==========================================

AGENTS = {
    "cv": cv_agent,
    "interview": interview_agent,
    "training": training_agent,
    "client": client_agent,
    "report": reporting_agent
}

# ==========================================
# Supervisor Prompt
# ==========================================

supervisor_prompt = ChatPromptTemplate.from_template("""
Anda adalah Supervisor Agent.

Tugas Anda adalah memilih agent yang paling sesuai.

Pilihan agent:

cv
interview
training
client
report

Jawab SATU KATA SAJA.

Question:
{question}
""")

supervisor_chain = (
    supervisor_prompt
    | llm
    | output_parser
)

# ==========================================
# Supervisor Agent
# ==========================================

def supervisor_agent(question):

    q = question.lower()

    # CV
    if any(keyword in q for keyword in [
        "cv",
        "screening",
        "resume"
    ]):
        selected = "cv"

    # Interview
    elif any(keyword in q for keyword in [
        "interview",
        "hr interview",
        "user interview"
    ]):
        selected = "interview"

    # Training
    elif any(keyword in q for keyword in [
        "training",
        "onboarding",
        "orientasi"
    ]):
        selected = "training"

    # Client
    elif any(keyword in q for keyword in [
        "client",
        "klien"
    ]):
        selected = "client"

    # Reporting
    elif any(keyword in q for keyword in [
        "laporan",
        "report",
        "ringkasan",
        "proses recruitment",
        "tahapan recruitment",
        "workflow"
    ]):
        selected = "report"

    else:
        selected = supervisor_chain.invoke({
            "question": question
        }).strip().lower()

        if selected not in AGENTS:
            selected = "report"

    result = AGENTS[selected](question)
    result["selected_agent"] = selected

    return result