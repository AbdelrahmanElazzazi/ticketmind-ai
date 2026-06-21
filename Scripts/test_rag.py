from dotenv import load_dotenv
from pinecone import Pinecone
from google import genai
import os
import time
import sys

load_dotenv()

# ======================
# Gemini Client
# ======================
gemini_client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ======================
# Pinecone Client
# ======================
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index("resolve-ticket-kb")

# ======================
# User Question
# ======================
question = "API Access videos?"

# ======================
# Create Question Embedding
# ======================
result = gemini_client.models.embed_content(model="gemini-embedding-2", contents=question)

question_vector = result.embeddings[0].values

# ======================
# Retrieve Top Chunks
# ======================
results = index.query(vector=question_vector, top_k=3, include_metadata=True)

context = ""

for match in results.matches:
    context += match.metadata["text"]
    context += "\n\n"

print("\nRETRIEVED CHUNKS:\n")

for match in results.matches:
    print("=" * 50)
    print("Score:", match.score)
    print("Source:", match.metadata["source"])
    
scores = [match.score for match in results.matches]

best_score = max(scores)

print(f"\nBest Score: {best_score:.4f}")

CONFIDENCE_THRESHOLD = 0.70

if best_score < CONFIDENCE_THRESHOLD:
    print("\nANSWER:")
    print("I couldn't find relevant information in the knowledge base.")
    raise SystemExit


# ======================
# Build Prompt
# ======================
prompt = f"""
You are a professional customer support assistant.

Your task:

1. Read the user's question.
2. Read the provided context.
3. Determine whether the context directly answers the user's question.

Rules:

- Use ONLY the provided context.
- Do NOT use your own knowledge.
- If the context does not directly answer the user's question, respond EXACTLY with:

the information is not available in the provided knowledge base.

- Do not guess.
- Do not infer missing information.
- Do not make assumptions.

Context:
{context}

Question:
{question}
"""

# ======================
# Generate Answer
# ======================
for attempt in range(3):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        break

    except Exception as e:
        print(f"Attempt {attempt + 1} failed")

        if attempt == 2:
            raise e

        time.sleep(5)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(response.text)