from pinecone import Pinecone
from dotenv import load_dotenv
from src.config import INDEX_NAME
import os

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(INDEX_NAME)


def upsert_chunks(records):
    """
    Upload records to Pinecone.
    """
    index.upsert(records)


def search(vector, top_k=3):
    """
    Search Pinecone for similar vectors.
    """
    return index.query(vector=vector, top_k=top_k, include_metadata=True)