# Implementation Roadmap

1.  **Architecture & Planning (DONE)**
    *   Tech stack selection
    *   Database schema design
    *   Topology design
    *   ADRs generated
2.  **Phase 1: Project Foundation**
    *   Initialize FastAPI + Aiogram structure
    *   Create `docker-compose.yml` for DB/Cache/Search
    *   Set up SQLAlchemy models and Alembic migrations
    *   Implement basic i18n
3.  **Phase 2: Users & Core Data**
    *   User registration and language selection flows in Bot
    *   Credit ledger models and logic
    *   Basic dataset models
4.  **Phase 3: Search Engine Integration**
    *   OpenSearch client integration
    *   Dataset indexing pipeline
    *   Bot search flow
5.  **Phase 4: Economy (Payments & Subs)**
    *   Telegram payments integration
    *   Subscription plan logic
6.  **Phase 5: Referrals**
    *   Referral code generation
    *   Reward logic on sign-up / purchase
7.  **Phase 6: Large Import System**
    *   Celery setup
    *   Chunked file reading (CSV/JSONL)
    *   Checkpointing system
8.  **Phase 7: Dataset Contributions**
    *   Quarantine upload flow
    *   Admin review logic
9.  **Phase 8: Broadcasts**
    *   Async broadcast worker tasks
    *   I18n support in broadcasts
10. **Phase 9: Observability & Hardening**
    *   Metrics (Prometheus)
    *   Rate limiting
11. **Phase 10: Deployment Wizard**
    *   Ansible playbook & bash script
    *   Scaling documentation
