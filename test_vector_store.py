from app.ingestion.loader import load_document
from app.ingestion.chunker import split_documents
from app.database.vector_store import (
    save_documents,
    search_documents
)

file_path = "uploaded_documents/company_policy.txt"

documents = load_document(file_path)

chunks = split_documents(documents)

save_documents(chunks)

print("Documents stored successfully!")

question = "How many annual leaves do employees get?"

results = search_documents(question)

for document, score in results:

    print("\nRetrieved content:")
    print(document.page_content)

    print("Metadata:")
    print(document.metadata)

    print("Distance score:")
    print(score)