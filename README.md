# Resolve AI Agent

AI-powered Zendesk Ticket Resolution System.

## Features
- Zendesk webhook integration
- RAG pipeline using Pinecone
- Gemini answer generation
- Human review queue
- Edit before approve workflow
- Auto reply to Zendesk tickets

## Tech Stack
- Python
- FastAPI
- Pinecone
- Google Gemini ( Flash 2.5 & Embedding -2)
- SQLite
- Zendesk API

## Project Structure
- `api.py` main FastAPI app
- `src/` core application code
- `Data/Knowledge_base/` knowledge base files
- `logs/` application logs

## Run Locally
```bash
pip install -r requirements.txt
uvicorn api:app --reload