from app.ingestion.loader import load_document

file_path = "uploaded_documents/company_policy.txt"

documents = load_document(file_path)

for document in documents:
    print("CONTENT:")
    print(document.page_content)

    print("\nMETADATA:")
    print(document.metadata)