
import re

from app.database.vector_store import (
    search_documents,
    get_uploaded_documents
)


CV_KEYWORDS = [
    "cv",
    "resume",
    "experience",
    "skills",
    "technologies",
    "technical skills",
    "education",
    "projects",
    "programming languages",
    "work history",
    "professional background"
]

POLICY_KEYWORDS = [
    "annual leave",
    "sick leave",
    "casual leave",
    "leave policy",
    "company policy",
    "employee policy",
    "working hours",
    "attendance",
    "notice period",
    "holiday",
    "holidays"
]

COMPARISON_KEYWORDS = [
    "compare",
    "comparison",
    "difference between",
    "both",
    "their differences"
]


def normalize_text(value):
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def identify_person(question):

    documents = get_uploaded_documents(document_type="cv")

    normalized_question = normalize_text(question)

    matched_documents = []

    for metadata in documents:

        person = metadata.get("person", "")
        document_id = metadata.get("document_id")

        if not person or not document_id:
            continue

        normalized_person = normalize_text(person)

        if normalized_person and re.search(
            r"\b" + re.escape(normalized_person) + r"\b",
            normalized_question
        ):
            matched_documents.append(document_id)

    return list(set(matched_documents))


def retrieve_documents(question):

    normalized_question = normalize_text(question)

    # Comparison questions should search across all CVs.
    if any(
        keyword in normalized_question
        for keyword in COMPARISON_KEYWORDS
    ):

        results = search_documents(
            question=question,
            document_type="cv",
            k=6
        )

    else:

        matched_document_ids = identify_person(question)

        # A person was identified: search only their document.
        if len(matched_document_ids) == 1:

            results = search_documents(
                question=question,
                document_id=matched_document_ids[0],
                k=4
            )

        # Multiple people were mentioned: search across CVs.
        elif len(matched_document_ids) > 1:

            results = search_documents(
                question=question,
                document_type="cv",
                k=8
            )

        # No person identified: infer the likely document category.
        elif any(
            keyword in normalized_question
            for keyword in CV_KEYWORDS
        ):

            results = search_documents(
                question=question,
                document_type="cv",
                k=4
            )

        elif any(
            keyword in normalized_question
            for keyword in POLICY_KEYWORDS
        ):

            results = search_documents(
                question=question,
                document_type="policy",
                k=4
            )

        else:

            results = search_documents(
                question=question,
                k=4
            )

    return [
        document
        for document, score in results
    ]
