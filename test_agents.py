from agents import cv_agent

result = cv_agent(
    "Apa saja kriteria screening CV?"
)

print("=" * 60)
print("Agent")
print(result["agent"])

print("\nJawaban")
print(result["answer"])

print("\nDokumen")

for doc in result["documents"]:
    print(
        f"{doc.metadata['source']} | Halaman {doc.metadata['page']}"
    )