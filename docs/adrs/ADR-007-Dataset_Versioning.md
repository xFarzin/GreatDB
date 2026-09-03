# ADR 007: Dataset Versioning

## Context
Updating a dataset shouldn't cause downtime or show half-imported results.

## Decision
Use OpenSearch **Index Aliases** combined with DB Version tracking.

## Rationale
*   Dataset `university` points to alias `dataset_university_active`.
*   Import writes to `dataset_university_v2`.
*   On success, Admin publishes. System atomically updates alias `dataset_university_active` to point to `dataset_university_v2`.
*   Zero downtime, safe rollback.
