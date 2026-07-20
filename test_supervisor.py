from supervisor import supervisor_agent

questions = [
    "Apa saja kriteria screening CV?",
    "Bagaimana proses interview kandidat?",
    "Bagaimana proses onboarding?",
    "Bagaimana update status kandidat kepada client?",
    "Apa saja tahapan proses recruitment?"
]

for q in questions:

    result = supervisor_agent(q)

    print("=" * 60)
    print("Question :", q)
    print("Selected Agent :", result["selected_agent"])
    print("Answer :", result["answer"][:150], "...")