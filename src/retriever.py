from src.embeddings import embed_text
from src.vector_store import search
from src.config import (CONFIDENCE_THRESHOLD, TOP_K)
from src.logger import logger


# Retriever Function
# -----------------
def retrieve_context(question,request_id=None,top_k=TOP_K):

    prefix = f"{request_id} | " if request_id else ""
    logger.info(f"{prefix}Retrieving Context | Top K = {top_k}")

    question_vector = embed_text(question)
    results = search(vector=question_vector,top_k=top_k)
    logger.info(f"{prefix}Pinecone Returned {len(results.matches)} Matches")

    if not results.matches:
        logger.warning(f"{prefix}No Matches Returned From Pinecone")

        return {
            "success": False,
            "best_score": 0,
            "context": None,
            "matches": []
        }

    scores = [match.score for match in results.matches]
    best_score = max(scores)

    logger.info(f"{prefix}Retriever Best Score = {best_score:.4f}")
    
    for match in results.matches:
        logger.info(f"{prefix}Match Score={match.score:.4f} | Source={match.metadata['source']}")

    if best_score < CONFIDENCE_THRESHOLD:
        logger.warning(f"{prefix}Score Below Threshold ({CONFIDENCE_THRESHOLD})")

    context = ""
    
    for match in results.matches:
        source = match.metadata["source"]
        text = match.metadata["text"]

        context += f"""
SOURCE: {source}

CONTENT:
{text}

"""

    return {
        "success": True,
        "best_score": best_score,
        "context": context,
        "matches": results.matches
    }