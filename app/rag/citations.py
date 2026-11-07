
import re


def extract_citations(answer, documents):
    """
    Extract only source references used in the answer.
    Source numbering must match the context numbering
    provided to the LLM.
    """

    cited_ids = set(
        int(source_id)
        for source_id in re.findall(
            r"\[Source\s+(\d+)\]",
            answer
        )
    )

    citations = []

    for source_id in sorted(cited_ids):

        if source_id < 0 or source_id >= len(documents):
            continue

        document = documents[source_id]

        metadata = document.metadata or {}

        page = metadata.get("page")

        if page is not None:
            page = int(page) + 1

        citations.append({
            "source_id": source_id,
            "source": metadata.get("source", "Unknown source"),
            "page": page,
            "content": document.page_content
        })

    return citations


def validate_citations(answer, citations):
    """
    Verify that every source ID referenced in the answer
    exists in the extracted citation list.
    """

    cited_ids = set(
        int(source_id)
        for source_id in re.findall(
            r"\[Source\s+(\d+)\]",
            answer
        )
    )

    available_ids = {
        citation["source_id"]
        for citation in citations
    }

    return bool(cited_ids) and cited_ids.issubset(available_ids)
