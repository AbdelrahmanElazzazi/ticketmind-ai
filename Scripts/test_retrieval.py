from dotenv import load_dotenv
from pinecone import Pinecone
from google import genai
import os

load_dotenv()

# Gemini
#-----------
gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Pinecone
#----------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index("resolve-ticket-kb")

question = "I forgot my password"

#----------------------
# Generate Question Embedding
#----------------------------
result = gemini_client.models.embed_content(model="gemini-embedding-2", contents=question)

question_vector = result.embeddings[0].values

# Search Pinecone
results = index.query(vector=question_vector, top_k=3, include_metadata=True)

print(results)