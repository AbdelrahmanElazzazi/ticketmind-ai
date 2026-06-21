import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag import ask

result = ask( "How to reset my password?" )

print("\nSuccess:", result["success"])
print("Best Score:", result["best_score"])

print("\nAnswer:\n")
print(result["answer"])
print("Review:", result["review_status"])