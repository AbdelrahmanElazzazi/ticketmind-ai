from dotenv import load_dotenv
import os

from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

result = client.models.embed_content(
    model="gemini-embedding-2",
    contents="How to reset a password"
)

vector = result.embeddings[0].values

print("Vector Length:", len(vector))

print("\nFirst 10 Values:")
print(vector[:10])