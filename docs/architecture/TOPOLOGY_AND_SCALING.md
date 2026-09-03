# Deployment Topology & Migration

## 2-Server Topology
*   **Server A (App & Frontend):** Nginx, FastAPI, Aiogram Bot, Celery Workers (light UI tasks), Redis.
*   **Server B (State & Data):** PostgreSQL, OpenSearch, MinIO (Storage).

## 3-Server Topology
*   **Server 1 (App):** Nginx, FastAPI, Aiogram Bot, Redis.
*   **Server 2 (Data):** PostgreSQL, OpenSearch.
*   **Server 3 (Workers & Storage):** Celery Workers (Heavy Imports), MinIO (Storage).

## 2-to-3 Server Migration Strategy
Because all state is externalized (PostgreSQL for SQL, OpenSearch for search, MinIO for files, Redis for tasks/cache), the App/Worker containers are 100% stateless.
Migration steps:
1. Spin up Server 3.
2. Update the environment variables on Server 3 to point to Server 2 (Postgres/OpenSearch) and Server 1 (Redis).
3. Deploy the Worker and MinIO containers on Server 3. (Sync MinIO data from A to 3 if moving storage).
4. Stop the heavy Worker container on Server A.
5. The system scales instantly without downtime or code changes.

## Deployment Wizard
We will use Ansible with a wizard script (`install.sh`). The wizard asks for roles (app, db, worker) and IP addresses, generating an inventory file and `.env` files, then runs `ansible-playbook` to configure the servers securely.
