import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.embeddings import embed_text
from src.vector_store import search

question = "I forgot my password"

question_vector = embed_text(question)

results = search(question_vector)

for match in results.matches:
    print("=" * 50)
    print("Score:", match.score)
    print("Source:", match.metadata["source"])