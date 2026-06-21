import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.review_queue import (initialize_database, add_to_review_queue)

initialize_database()

add_to_review_queue(
    request_id="REQ-123",
    question="I forgot my password",
    answer="Reset your password...",
    context="Password Reset Procedure...",
    score=0.75
)

print("Done")