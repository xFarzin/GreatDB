# ADR 002: Search Engine Choice

## Context
The platform needs to search potentially hundreds of millions of records (hundreds of gigabytes) with low latency. PostgreSQL is not suitable for full-text search across arbitrary massive schemaless datasets at this scale.

## Decision
We will use **OpenSearch** (specifically 2.x).

## Rationale
*   Apache 2.0 licensed, avoiding Elasticsearch's SSPL license complexities, making it easier for users to self-host cleanly.
*   Horizontally scalable via sharding.
*   Excellent integration with Python.
*   Supports aliases, which perfectly fits our "Dataset Versioning" requirement (atomic swaps of indices).
