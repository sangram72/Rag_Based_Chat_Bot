from app.rag.retriever import retrieve_documents


question = "How many vacation days do employees get?"

documents = retrieve_documents(question)

print("Retrieved documents:", len(documents))

for index, document in enumerate(documents):

    print(f"\nDocument {index + 1}")

    print("Content:")
    print(document.page_content)

    print("Source:")
    print(document.metadata.get("source"))