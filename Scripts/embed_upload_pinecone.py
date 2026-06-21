from dotenv import load_dotenv
from pinecone import Pinecone
from google import genai

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from pathlib import Path
import os

# ==========================
# Load Environment Variables
# ==========================
load_dotenv()

# =============
# Gemini API
# ==========
gemini_client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ==================
# Pinecone API
# ==========================
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("resolve-ticket-kb")

# =====================
# Load Documents
# ====================
knowledge_base_path = Path("Data/Knowledge_base")

documents = []

for file in knowledge_base_path.glob("*.txt"):
    loader = TextLoader( str(file), encoding="utf-8" )

    docs = loader.load()
    documents.extend(docs)

# ==========================
# Chunk Documents
# ==========================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"Chunks Loaded: {len(chunks)}")

# ==========================
# Create Vectors ( Embeddings )
# ========================
vectors = []

for i, chunk in enumerate(chunks):

    result = gemini_client.models.embed_content(model="gemini-embedding-2", contents=chunk.page_content)

    embedding = result.embeddings[0].values

    vectors.append({
        "id": f"chunk_{i}",
        "values": embedding,
        "metadata": {
            "source": chunk.metadata.get("source", ""),
            "text": chunk.page_content
        }
    })

    print(f"Embedded Chunk {i+1}/{len(chunks)}")

# ==========================
# Upload to Pinecone
# ==========================
index.upsert(vectors=vectors)

print("\nUpload Complete!")
print(f"Uploaded {len(vectors)} vectors.")