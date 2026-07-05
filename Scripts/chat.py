import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag import ask

print("=" * 50)
print("TicketMind AI Assistant")
print("Type 'exit' to quit")
print("=" * 50)

while True:
    question = input("\nPlease write your question: ")

    if question.lower() == "exit":
        break

    result = ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nConfidence:")
    print(round(result["best_score"], 4))

    print("\nReview Status:")
    print(result["review_status"])

    print("\n" + "=" * 50)