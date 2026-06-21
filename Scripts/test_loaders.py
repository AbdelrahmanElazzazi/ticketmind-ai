import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.loaders import load_documents
from src.loaders import chunk_documents


documents = load_documents()

print("Documents:", len(documents))

chunks = chunk_documents(documents)

print("Chunks:", len(chunks))