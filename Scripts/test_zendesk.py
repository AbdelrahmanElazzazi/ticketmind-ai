import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.zendesk_client import get_ticket


ticket = get_ticket(2)

print(ticket)