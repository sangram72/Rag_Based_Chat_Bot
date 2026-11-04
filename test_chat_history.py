
from app.graph.workflow import create_workflow

workflow = create_workflow()

# Same thread_id for both questions
config = {
    "configurable": {
        "thread_id": "conversation_test_001"
    }
}

# First question
result1 = workflow.invoke(
    {
        "question": "How many annual leave days are employees entitled to?"
    },
    config=config
)

print("\nUSER 1: How many annual leave days are employees entitled to?")
print("AI 1:", result1["answer"])


# Follow-up question
result2 = workflow.invoke(
    {
        "question": "Who approves it?"
    },
    config=config
)

print("\nUSER 2: Who approves it?")
print("AI 2:", result2["answer"])


# Display complete conversation history
saved_state = workflow.get_state(config)

print("\n========== CHAT HISTORY ==========")

for message in saved_state.values["messages"]:
    print(f"\n{message.type.upper()}:")
    print(message.content)
