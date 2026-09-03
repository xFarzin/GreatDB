# Missing Production Requirements Identified

While the spec is comprehensive, standard production systems require:
1.  **Log Aggregation:** Standard stdout is good for Docker, but a centralized log system (like Promtail/Loki or ELK) might be needed at 3+ servers. We will stick to structured JSON logs to standard out, compatible with any shipper.
2.  **Backups (Implementation Detail):** The spec mentions backups. We need a cron-based pg_dump and OpenSearch snapshot strategy.
3.  **Connection Pooling:** PgBouncer is necessary if the FastAPI app and multiple Celery workers spawn hundreds of connections to Postgres. We will include PgBouncer in the docker-compose.
