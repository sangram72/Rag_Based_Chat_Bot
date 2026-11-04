from app.rag.retriever import retrieve_documents

from app.rag.generator import generate_answer

from app.rag.citations import (
    extract_citations,
    validate_citations
)


question = "How many annual leaves do employees get?"

documents = retrieve_documents(question)

citations = extract_citations(documents)

answer = generate_answer(question, documents)

is_valid = validate_citations(
    answer,
    citations
)

print("\nAI ANSWER:")
print(answer)

print("\nCITATIONS:")
print(citations)

print("\nVALIDATION:")
print(is_valid)


if not is_valid:

    print("Answer rejected: Valid citations are missing.")