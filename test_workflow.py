
from app.graph.workflow import create_workflow

workflow = create_workflow()

# Identify this conversation
config = {
    "configurable": {
        "thread_id": "test_user_001"
    }
}

result = workflow.invoke(
    {
        "question": "How many annual leaves do employees get?",
        "documents": [],
        "answer": "",
        "citations": [],
        "is_valid": False
    },
    config=config
)

print("\nAI ANSWER:")
print(result["answer"])

print("\nCITATIONS:")
print(result["citations"])

print("\nVALIDATION:")
print(result["is_valid"])

# Check saved conversation state
saved_state = workflow.get_state(config)

print("\nSAVED STATE:")
print(saved_state.values)
