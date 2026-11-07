
from langchain_core.messages import HumanMessage, AIMessage

from app.rag.retriever import retrieve_documents
from app.rag.generator import generate_answer
from app.rag.citations import (
    extract_citations,
    validate_citations
)


def retrieve_node(state):
    """
    Retrieve relevant document chunks.
    """

    question = state["question"]

    documents = retrieve_documents(question)

    return {
        "documents": documents,
        "generation_attempts": 0
    }


def check_retrieval_node(state):
    """
    Check whether relevant documents were found.
    """

    documents = state.get("documents", [])

    if not documents:
        return {
            "answer": "I couldn't find relevant information in the uploaded documents.",
            "citations": [],
            "is_valid": True
        }

    return {}


def generate_node(state):
    """
    Generate an answer using retrieved documents.
    """

    question = state["question"]
    documents = state.get("documents", [])

    attempts = state.get("generation_attempts", 0) + 1

    answer = generate_answer(
        question=question,
        documents=documents,
        chat_history=state.get("messages", [])
    )

    citations = extract_citations(
        answer=answer,
        documents=documents
    )

    return {
        "answer": answer,
        "citations": citations,
        "generation_attempts": attempts,
        "messages": [
            HumanMessage(content=question),
            AIMessage(content=answer)
        ]
    }


def validate_node(state):
    """
    Validate citation references.
    """

    answer = state.get("answer", "")
    citations = state.get("citations", [])

    is_valid = validate_citations(
        answer=answer,
        citations=citations
    )

    return {
        "is_valid": is_valid
    }
