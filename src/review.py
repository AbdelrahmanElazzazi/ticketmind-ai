from src.config import (AUTO_APPROVE_THRESHOLD, HUMAN_REVIEW_THRESHOLD)

def review_decision(score):

    if score >= AUTO_APPROVE_THRESHOLD:
        return "AUTO_APPROVED"

    elif score >= HUMAN_REVIEW_THRESHOLD:
        return "NEEDS_HUMAN_REVIEW"

    return "NO_RELEVANT_INFORMATION"