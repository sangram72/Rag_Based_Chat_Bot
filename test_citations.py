from app.rag.retriever import retrieve_documents
from app.rag.citations import extract_citations

question = "How many annual leaves do employees get?"

documents = retrieve_documents(question)

citations = extract_citations(documents)

for citation in citations:

    print("\nCitation:")
    print("Source ID:", citation["source_id"])
    print("Source:", citation["source"])
    print("Page:", citation["page"])
    print("Evidence:", citation["content"])