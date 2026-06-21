import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.embeddings import embed_text

vector = embed_text("How do I reset my password?")

print(type(vector))
print(len(vector))
print(vector[:5])