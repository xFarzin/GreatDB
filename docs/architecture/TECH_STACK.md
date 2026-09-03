# Technology Stack Proposal

## Core Application
*   **Language:** Python 3.12+
*   **API Framework:** FastAPI (high performance, async, built-in validation with Pydantic).
*   **Bot Framework:** aiogram 3.x (modern, fully asynchronous Telegram bot API framework for Python).
*   **Worker/Task Queue:** Celery (reliable, production-tested for chunked background tasks and broadcasts) or SAQ (simple async queue) if purely async is preferred. Celery + Redis is industry standard for long imports.
*   **Localization:** GNU gettext / Babel for backend strings + aiogram's i18n middlewares.

## Data & Storage
*   **Primary Database:** PostgreSQL 16+ (ACID compliance, solid for credit ledgers and transactional state).
*   **Search Engine:** OpenSearch 2.x (Apache 2.0 fork of Elasticsearch, perfect for Docker deployments without licensing headaches, highly scalable).
*   **Cache & Queue Broker:** Redis (Rate limiting, Celery broker, transient bot state).
*   **Object Storage:** MinIO (S3-compatible, for storing massive raw CSV/JSON uploads before processing, isolating large files from the DB).

## Infrastructure & DevOps
*   **Containerization:** Docker & Docker Compose.
*   **Web Server / Proxy:** Caddy or Nginx (Caddy offers automatic HTTPS which is great for Telegram webhooks).
*   **Configuration:** Ansible (for the deployment wizard and multi-server orchestration).
*   **Monitoring:** Prometheus + Grafana (system health, custom metrics for searches, bot activity).
