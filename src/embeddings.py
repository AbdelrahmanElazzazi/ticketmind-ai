from dotenv import load_dotenv
from google import genai
from src.config import EMBEDDING_MODEL
import os


#---------------
# Load Gemini Embeddings
#------------------
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def embed_text(text):
    """
    Generate Gemini embedding for text.
    """

    result = client.models.embed_content(model=EMBEDDING_MODEL, contents=text)

    return result.embeddings[0].values