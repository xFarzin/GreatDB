# ADR 001: Database Choice

## Context
We need a robust relational database for the platform's core entities: users, credit ledger, subscriptions, jobs, and metadata.

## Decision
We will use **PostgreSQL**.

## Rationale
*   ACID compliant, which is strictly required for the credit ledger (financial transactions).
*   Supports advanced JSON/JSONB features for flexible metadata storage without NoSQL.
*   Highly scalable with excellent connection pooling (PgBouncer).
