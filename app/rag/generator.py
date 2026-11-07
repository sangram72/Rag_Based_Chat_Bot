
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


SYSTEM_PROMPT = """
You are a document-based RAG assistant.

RULES:

1. Answer questions using ONLY the provided document context.
2. Do not use external knowledge or invent information.
3. Every factual claim must have a supporting citation.
4. Use the exact source numbers provided in the context.
5. Never change, guess, or invent source numbers.
6. Do not cite a source unless its content supports the claim.
7. If the answer is unavailable in the documents, clearly say so.
8. Keep answers clear and concise.
9. Do not claim that something is inferred when it is not explicitly supported.
10. Do not create quotations that differ from the document text.

CITATION FORMAT:

Use this exact format:

[Source 0]
[Source 1]

Only use source IDs present in the supplied context.
"""


def generate_answer(question, documents, chat_history=None):

    context = ""

    for index, document in enumerate(documents):

        metadata = document.metadata or {}

        context += f"""
[Source {index}]
Filename: {metadata.get("filename", metadata.get("source", "Unknown"))}
Page: {metadata.get("page", "Unknown")}
Content:
{document.page_content}

-------------------------
"""

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT + "\n\nDOCUMENT CONTEXT:\n" + context
        )
    ]

    if chat_history:

        for message in chat_history:

            if getattr(message, "type", None) in ["human", "ai"]:
                messages.append(message)

    messages.append(
        HumanMessage(content=question)
    )

    response = llm.invoke(messages)

    return response.content
