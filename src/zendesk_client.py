import requests
from dotenv import load_dotenv
import os

load_dotenv()

ZENDESK_SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
ZENDESK_EMAIL = os.getenv("ZENDESK_EMAIL")
ZENDESK_API_TOKEN = os.getenv("ZENDESK_API_TOKEN")

BASE_URL = f"https://{ZENDESK_SUBDOMAIN}.zendesk.com/api/v2"

# Get Ticket Details
#-----------------
def get_ticket(ticket_id):
    url = f"{BASE_URL}/tickets/{ticket_id}.json"

    response = requests.get(url, auth=(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN))
    response.raise_for_status()

    return response.json()

# Add Comments to Ticket
#----------------------
def add_comment_to_ticket(ticket_id, comment):
    url = f"{BASE_URL}/tickets/{ticket_id}.json"
    payload = {
        "ticket": {
            "comment": {
                "body": comment,
                "public": True
            }
        }
    }
    response = requests.put(url, json=payload, auth=(f"{ZENDESK_EMAIL}/token", ZENDESK_API_TOKEN))
    response.raise_for_status()
    
    return response.json()