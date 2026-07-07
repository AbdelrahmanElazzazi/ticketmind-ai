---
Title: API Reference
Project: TicketMind
Version: 1.0
Last Updated: July 2026
---

# 📚 API Reference

## Overview

TicketMind exposes a RESTful API built with FastAPI to manage AI-powered ticket processing, human review workflows, monitoring, and health checks.

Interactive API documentation is available through Swagger UI.

```
http://localhost:8001/docs
```

---

# Base URL

```
http://localhost:8001
```

---

# Health & Monitoring

## GET /

Returns the API status.

### Response

```json
{
    "status": "running",
    "service": "TicketMind API"
}
```

---

## GET /health

Checks application health.

### Response

```json
{
    "status": "healthy"
}
```

---

## GET /metrics

Returns Prometheus metrics for monitoring.

---

# AI Endpoints

## POST /ask

Generates an AI response using the RAG pipeline.

### Request

```json
{
    "question": "How can I reset my password?"
}
```

### Response

```json
{
    "answer": "...",
    "review_status": "AUTO_APPROVED"
}
```

---

# Zendesk Integration

## POST /zendesk/ticket

Processes Zendesk tickets.

### Request

```json
{
    "ticket_id": 101,
    "subject": "Password Reset",
    "description": "I cannot reset my password."
}
```

---

## POST /webhook/zendesk

Webhook endpoint triggered automatically by Zendesk.

This endpoint starts the complete AI workflow:

- Ticket Processing
- Embedding Generation
- Pinecone Retrieval
- Gemini Response Generation
- Confidence Evaluation
- Auto Reply or Human Review

---

# Review Queue

## GET /review-queue

Returns all pending reviews.

---

## GET /review-queue/{review_id}

Returns a specific review.

---

## PUT /review-queue/{review_id}

Updates the AI-generated answer before approval.

### Request

```json
{
    "answer": "Updated response..."
}
```

---

## POST /review-queue/{review_id}/approve

Approves the response and publishes it to Zendesk.

---

## POST /review-queue/{review_id}/reject

Rejects the pending review.

---

# API Workflow

```
Zendesk
      │
      ▼
Webhook
      │
      ▼
FastAPI
      │
      ▼
RAG Pipeline
      │
      ▼
AI Response
      │
 ┌────┴─────┐
 ▼          ▼

Auto     Human Review
Reply       Queue
```

---

# Authentication

Current Version:

- Local Development
- API Keys stored in `.env`

Future versions may support:

- JWT Authentication
- OAuth2
- Role-Based Access Control (RBAC)

---

# Error Responses

| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 400 | Invalid Request |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

---

# Interactive Documentation

Swagger UI

```
http://localhost:8001/docs
```

---

# Next Documentation

Continue with:

- 07-Future-Roadmap.md