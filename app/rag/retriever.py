from app.database.vector_store import search_documents


def retrieve_documents(question):

    results = search_documents(question)

    documents = [
        document
        for document, score in results
    ]

    return documents