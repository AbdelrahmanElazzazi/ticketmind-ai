from google import genai
from dotenv import load_dotenv
import os
import time
from src.metrics import (tickets_total, auto_approved_total, human_review_total, rejected_total,response_time_seconds)
from src.retriever import retrieve_context
from src.prompt_builder import build_prompt
from src.review import review_decision
from src.config import LLM_MODEL
from src.logger import logger
from src.review_queue import add_to_review_queue

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def ask(question, subject=None, request_id=None, ticket_id=None):
    start_time = time.time()
    tickets_total.inc()
    prefix = f"{request_id} | " if request_id else ""
    logger.info(f"{prefix}Question Received: {question}")
    
    full_question = question
    if subject:
        full_question = f"""
        Subject: {subject}
        
        Description:
        {question}
        """
    logger.info(f"{prefix}Full Question:\n{full_question}")    
    retrieval_result = retrieve_context(full_question, request_id=request_id)

    logger.info(f"{prefix}Best Score: {retrieval_result['best_score']}")

    if not retrieval_result["success"]:
        elapsed_time = round(time.time() - start_time, 2)
        rejected_total.inc()
        response_time_seconds.observe(elapsed_time)
        logger.warning(f"{prefix}No relevant context found")
        logger.info(f"{prefix}Execution Time: {elapsed_time}s")

        return {
            "request_id": request_id,
            "success": False,
            "best_score": retrieval_result["best_score"],
            "review_status": "REJECTED",
            "answer": "I couldn't find relevant information in the knowledge base."
        }

    prompt = build_prompt(question=full_question,context=retrieval_result["context"])

    for attempt in range(3):
        try:
            response = client.models.generate_content(model=LLM_MODEL,contents=prompt)
            decision = review_decision(retrieval_result["best_score"])
            if decision == "AUTO_APPROVED":
                auto_approved_total.inc()
            elif decision == "NEEDS_HUMAN_REVIEW":
                human_review_total.inc()
            else:
                rejected_total.inc()
            
            if decision == "NEEDS_HUMAN_REVIEW":
                logger.info(f"{request_id} | Adding Ticket To Human Review Queue")
                add_to_review_queue(
                    ticket_id=ticket_id,
                    request_id=request_id,
                    question=question,
                    answer=response.text,
                    context=retrieval_result["context"],
                    score=retrieval_result["best_score"]
                )
            logger.info(f"{prefix}Review Status: {decision}")

            sources = []

            for match in retrieval_result["matches"]:
                sources.append(match.metadata["source"])

            sources = list(set(sources))

            elapsed_time = round(time.time() - start_time, 2)
            response_time_seconds.observe(elapsed_time)
            logger.info(f"{prefix}Sources: {sources}")
            logger.info(f"{prefix}Execution Time: {elapsed_time}s")
            logger.info(f"{prefix}Answer Generated Successfully")

            return {
                "request_id": request_id,
                "success": True,
                "best_score": retrieval_result["best_score"],
                "review_status": decision,
                "sources": sources,
                "answer": response.text
            }

        except Exception:
            logger.exception(f"{prefix}Gemini Generation Failed - Attempt {attempt + 1}")
            if attempt == 2:
                raise

            time.sleep(5)