from src.rag import ask
from src.logger import logger
from src.zendesk_client import add_comment_to_ticket
from src.metrics import (tickets_total, auto_approved_total, human_review_total, no_relevant_info_total)


def process_zendesk_webhook(ticket_id,subject,description,request_id):
    print("WEBHOOK RECEIVED")
    logger.warning(f"{request_id} | WEBHOOK RECEIVED | Ticket={ticket_id}")
    logger.info(f"{request_id} | Processing Zendesk Webhook | Ticket={ticket_id}")
    tickets_total.inc()
    
    result = ask(question=description, subject=subject, request_id=request_id, ticket_id=ticket_id)
    
    review_status = result["review_status"]
    
    if review_status == "AUTO_APPROVED":
        auto_approved_total.inc()
        add_comment_to_ticket(ticket_id=ticket_id, comment=result["answer"])
        logger.info(f"{request_id} | Auto Reply Added To Ticket {ticket_id}")
    
    elif review_status == "NEEDS_HUMAN_REVIEW":
        human_review_total.inc()
        logger.info(f"{request_id} | Sent To Human Review Queue")

    elif review_status == "NO_RELEVANT_INFORMATION":
        no_relevant_info_total.inc()
        logger.warning(f"{request_id} | No Relevant Information Found")