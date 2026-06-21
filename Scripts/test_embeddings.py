from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)

text = "How to reset a password"

vector = embeddings.embed_query(text)

print("Vector Type:", type(vector))
print("Vector Length:", len(vector))

print("\nFirst 10 Values:")
print(vector[:10])