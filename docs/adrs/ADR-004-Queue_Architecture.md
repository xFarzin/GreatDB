# ADR 004: Queue Architecture

## Context
Imports must be asynchronous, chunked, resumable, and lower priority than user searches.

## Decision
We will use **Redis + Celery** (or equivalent task queue like Arq/SAQ).

## Rationale
*   Redis provides fast, persistent queuing.
*   Celery supports task routing (e.g., `telegram_tasks` vs `heavy_imports`), allowing us to enforce strict priority and resource limits.
*   Supports rate-limiting and robust retries natively.
