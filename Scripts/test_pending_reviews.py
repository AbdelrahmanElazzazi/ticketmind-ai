import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from src.review_queue import get_pending_reviews

reviews = get_pending_reviews()

for review in reviews:
    print(review)