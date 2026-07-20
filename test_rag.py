from rag import rag_answer

result = rag_answer(
    "Apa saja tahapan proses recruitment?"
)

print(result["answer"])