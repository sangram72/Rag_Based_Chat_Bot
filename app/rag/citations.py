
import re


def validate_citations(answer, citations):

    valid_ids = {
        citation["source_id"]
        for citation in citations
    }

    used_ids = re.findall(
        r"\[Source (\d+)\]",
        answer
    )

    if not used_ids:
        return False

    for source_id in used_ids:

        if int(source_id) not in valid_ids:
            return False

    return True


def extract_citations(documents):

    citations = []

    for index, document in enumerate(documents):

        citation = {
            "source_id": index,
            "source": document.metadata.get("source"),
            "page": (
                document.metadata.get("page", None) + 1
                if document.metadata.get("page") is not None
                else None
            ),
            "content": document.page_content
        }

        citations.append(citation)

    return citations