from langchain_community.document_loaders import TextLoader
from pathlib import Path

knowledge_base_path = Path("Data/Knowledge_base")

documents = []

for file in knowledge_base_path.glob("*.txt"):
    loader = TextLoader(str(file), encoding="utf-8")
    docs = loader.load()
    documents.extend(docs)

print(f"Loaded {len(documents)} documents")

for doc in documents:
    print("-" * 50)
    print(doc.metadata["source"])