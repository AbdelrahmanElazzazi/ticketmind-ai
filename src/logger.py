import logging
import os
import uuid

def generate_request_id():
    return f"REQ-{uuid.uuid4().hex[:8]}"

os.makedirs("logs", exist_ok=True)

file_handler = logging.FileHandler(
    "logs/app.log",
    encoding="utf-8"
)

console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        file_handler,
        console_handler
    ],
    force=True
)
logger = logging.getLogger("resolve-ticket")