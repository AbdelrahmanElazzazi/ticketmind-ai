import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.retriever import retrieve_context

result = retrieve_context("I forgot my password")

print("Success:", result["success"])
print("Best Score:", result["best_score"])

print("\nContext:\n")

print(result["context"])