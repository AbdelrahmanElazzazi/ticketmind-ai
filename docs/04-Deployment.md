---
Title: Deployment
Project: TicketMind
Version: 1.0
Last Updated: July 2026
---

# 🚀 Deployment Guide

## Overview

TicketMind is fully containerized using Docker and Docker Compose, making it easy to deploy and run the complete application stack.

The project includes:

- FastAPI Backend
- Prometheus Monitoring
- Grafana Dashboard
- ngrok Tunnel (for Zendesk Webhooks)

---

# Project Structure

```

TicketMind/
│
├── docker/
│ ├── Dockerfile
│ ├── docker-compose.yml
│ └── prometheus.yml
│
├── src/
├── docs/
├── requirements.txt
├── api.py
└── .env

```

---

# Prerequisites

Before running the project, ensure the following are installed:

- Python 3.12+
- Docker Desktop
- Docker Compose
- ngrok
- Git

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=xxxxxxxxxxxxxxxx
PINECONE_API_KEY=xxxxxxxxxxxxxxxx
PINECONE_INDEX_NAME=ticketmind
ZENDESK_SUBDOMAIN=your_subdomain
ZENDESK_EMAIL=your_email
ZENDESK_API_TOKEN=your_token
```

---

# Build Containers

Navigate to the Docker directory.

```bash
cd docker
```

Build and start all services.

```bash
docker compose up --build
```

To stop the services:

```bash
docker compose down
```

---

# Available Services

| Service | URL |
|----------|-----------------------------|
| FastAPI | http://localhost:8001 |
| Swagger UI | http://localhost:8001/docs |
| Health Check | http://localhost:8001/health |
| Metrics | http://localhost:8001/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 |

---

# Configure ngrok

Expose the FastAPI application:

```bash
ngrok http 8001
```

Copy the generated HTTPS URL.

Example:

```
https://xxxxxxxx.ngrok-free.app
```

Use this URL as the Zendesk Webhook endpoint.

```
https://xxxxxxxx.ngrok-free.app/webhook/zendesk
```

---

# Verify Deployment

Confirm the following:

- FastAPI is running
- Swagger UI loads successfully
- Prometheus target status is **UP**
- Grafana connects successfully to Prometheus
- Zendesk webhook reaches the FastAPI service
- AI responses are generated correctly

---

# Monitoring

Application metrics are available at:

```
/metrics
```

Collected metrics include:

- Total Tickets
- Auto Approved Tickets
- Human Review Tickets
- Rejected Tickets
- Average Response Time

These metrics are visualized in Grafana dashboards.

---

# Troubleshooting

## Port Already in Use

Update the exposed ports in `docker-compose.yml`.

Example:

```yaml
ports:
  - "8001:8000"
```

---

## Prometheus Target Down

Verify:

- FastAPI is running
- `/metrics` endpoint is accessible
- `prometheus.yml` targets the correct container

---

## Zendesk Webhook Not Triggered

Verify:

- ngrok is running
- Webhook URL is correct
- Zendesk Trigger is active

---

# Next Documentation

Continue with:

- 05-Monitoring.md