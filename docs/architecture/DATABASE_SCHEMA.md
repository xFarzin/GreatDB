# Database Schema Proposal (PostgreSQL)

## Users & Profiles
*   `users`: id, telegram_id (unique), language (en/fa), is_active, created_at, updated_at
*   `admin_users`: id, user_id (fk), role (SUPER_ADMIN, ADMIN, SUPPORT)

## Datasets
*   `datasets`: id, name_en, name_fa, desc_en, desc_fa, status, visibility, searchable, record_count, created_at
*   `dataset_versions`: id, dataset_id, version_num, index_name (OpenSearch alias), is_active
*   `dataset_submissions`: id, user_id, status (QUARANTINED, APPROVED, REJECTED), file_path (MinIO)

## Imports
*   `imports`: id, dataset_id, version_id, status, file_path, total_bytes, bytes_processed, total_records, records_processed, error_log
*   `import_checkpoints`: import_id (fk, pk), chunk_index, byte_offset, status

## Economy (Credits & Subs)
*   `credit_transactions` (Append-only ledger): id, user_id, amount, tx_type (PURCHASE, SEARCH, REFERRAL, etc.), reference_id, created_at
*   `subscriptions`: id, user_id, plan_id, start_date, end_date, is_active
*   `payments`: id, user_id, provider_charge_id, amount, currency, status (PENDING, SUCCESS, FAILED), idempotency_key

## Referrals
*   `referrals`: id, referrer_id, referred_id, created_at
*   `referral_rewards`: id, referral_id, reward_type, credit_transaction_id

## Telemetry
*   `search_logs`: id, user_id, dataset_id, query_hash, duration_ms, success, credits_charged
*   `audit_logs`: id, admin_id, action, target_table, target_id, details (JSON)
