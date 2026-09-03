# ADR 003: Storage Architecture

## Context
Users and admins will upload large CSV/JSON datasets (up to hundreds of GBs). We need to store these reliably while workers stream them.

## Decision
We will use **MinIO** (S3-compatible object storage).

## Rationale
*   Keeps massive files out of the PostgreSQL DB.
*   S3 API standard means we can easily swap to AWS S3, Cloudflare R2, or DigitalOcean Spaces if the deployment moves to the cloud.
*   Supports multipart uploads natively (great for the Admin Panel).
