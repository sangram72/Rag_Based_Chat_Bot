from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

system_prompt = """
You are a document-based AI assistant.

Answer only using the provided document context.

Use previous conversation messages to understand follow-up questions.

Every factual claim must include a citation in this format:
[Source 0]

Only use source IDs provided in the current document context.

If the answer is unavailable, say:
"I could not find sufficient information in the provided documents."

Never invent information or citations.

Document context:
{context}
"""

def generate_answer(question, documents, chat_history=None):

    if chat_history is None:
        chat_history = []

    context = "\n\n".join(
        [
            f"[Source {index}]\n{doc.page_content}"
            for index, doc in enumerate(documents)
        ]
    )

    messages = [
        SystemMessage(
            content=system_prompt.format(context=context)
        )
    ]

    messages.extend(chat_history)

    from langchain_core.messages import HumanMessage

    messages.append(
        HumanMessage(content=question)
    )

    response = llm.invoke(messages)

    return response.content