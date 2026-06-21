from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------
# Load Documents
# ---------------

knowledge_base_path = Path("Data/Knowledge_base")

documents = []

for file in knowledge_base_path.glob("*.txt"):
    loader = TextLoader(str(file), encoding="utf-8")

    docs = loader.load()
    documents.extend(docs)

print("=" * 50)
print(f"Documents Loaded: {len(documents)}")
print("=" * 50)

# -------------------
# Validate Documents
# -------------------

for i, doc in enumerate(documents):
    print(f"\nDocument {i + 1}")
    print(f"Source: {doc.metadata['source']}")
    print(f"Length: {len(doc.page_content)} characters")

# -----------
# Chunking
# -------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print("\n" + "=" * 50)
print(f"Total Chunks: {len(chunks)}")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1}")
    print("Length:", len(chunk.page_content))

# -----------------------
# Preview First Chunk
# ---------------------

if chunks:
    print("\nFirst Chunk:\n")
    print(chunks[0].page_content)

    print("\nMetadata:\n")
    print(chunks[0].metadata)
else:
    print("\nNo chunks were generated.")
    
#-----------------
# Test 
#----------------------
#print(type(chunks))
#print(len(chunks))
#print(type(chunks[0]))