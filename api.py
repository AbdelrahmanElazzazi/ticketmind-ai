from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import Response
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

from src.rag import ask
from src.models import (QuestionRequest, ZendeskTicket, ReviewUpdate)
from src.logger import logger, generate_request_id
from src.review_queue import (get_pending_reviews, get_review_by_id, approve_review, reject_review, update_review_answer, get_review_for_approval)
from src.webhook import process_zendesk_webhook
from src.zendesk_client import add_comment_to_ticket

app = FastAPI(title="Resolve Ticket API", version="1.0.0")

from src.review_queue import initialize_database

initialize_database()

@app.get("/")
def home():

    return {
        "status": "running",
        "service": "Resolve Ticket API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.post("/ask")
def ask_question(request: QuestionRequest):
    request_id = generate_request_id()
    logger.info(f"{request_id} | Incoming API Request: {request.question}")

    try:
        result = ask(request.question, request_id=request_id)
        return result

    except Exception as e:
        logger.exception(f"{request_id} | API Error")

        raise HTTPException(status_code=500,detail=str(e))

# Process Zendesk Ticket Webhook
#------------------------
@app.post("/zendesk/ticket")
def process_zendesk_ticket(ticket: ZendeskTicket):
    request_id = generate_request_id()

    try:
        return process_zendesk_webhook(
            ticket_id=ticket.ticket_id,
            subject=ticket.subject,
            description=ticket.description,
            request_id=request_id
        )

    except Exception as e:
        logger.exception(f"{request_id} | Zendesk Ticket Processing Failed")

        raise HTTPException(status_code=500, detail=str(e))

# Webhook Endpoint for Zendesk
#------------------------
@app.post("/webhook/zendesk")
def zendesk_webhook(ticket: ZendeskTicket):
    request_id = generate_request_id()
    logger.warning(f"{request_id} | WEBHOOK RECEIVED | "f"Ticket={ticket.ticket_id} | "f"Subject={ticket.subject}")

    try:
        return process_zendesk_webhook(
            ticket_id=ticket.ticket_id,
            subject=ticket.subject,
            description=ticket.description,
            request_id=request_id
        )

    except Exception as e:
        logger.exception(f"{request_id} | Webhook Processing Failed")

        raise HTTPException(status_code=500, detail=str(e))

# Approve Ticket From Review Queue
#----------------------------
@app.post("/review-queue/{review_id}/approve")
def approve_ticket(review_id: int):

    review = get_review_for_approval(review_id)

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review Not Found"
        )

    add_comment_to_ticket(
        ticket_id=review["ticket_id"],
        comment=review["answer"]
    )

    approve_review(review_id)

    return {
        "success": True,
        "review_id": review_id,
        "ticket_id": review["ticket_id"],
        "status": "APPROVED"
    }

# Review Queue Endpoints
#-------------------------
@app.get("/review-queue")
def review_queue():

    reviews = get_pending_reviews()

    return {
        "count": len(reviews),
        "reviews": reviews
    }

# Check Spacific Review By ID
#-----------------------
@app.get("/review-queue/{review_id}")
def get_review(review_id: int):

    review = get_review_by_id(review_id)

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review

# Reject The Review By ID
#---------------------------
@app.post("/review-queue/{review_id}/reject")
def reject(review_id: int):

    reject_review(review_id)

    return {
        "message": "Review rejected",
        "review_id": review_id
    }

# Update/Edit The Review Answer By ID
#--------------------------
@app.put("/review-queue/{review_id}")
def update_review(
    review_id: int,
    review_update: ReviewUpdate
):

    review = get_review_by_id(review_id)

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    update_review_answer(review_id=review_id, answer=review_update.answer)

    return {
        "message": "Review updated successfully",
        "review_id": review_id
    }
