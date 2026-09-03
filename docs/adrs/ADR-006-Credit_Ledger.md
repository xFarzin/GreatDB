# ADR 006: Credit Ledger

## Context
Credit balances must be perfectly consistent, supporting concurrent deductions, refunds, and additions.

## Decision
We will implement an **Append-Only Ledger** in PostgreSQL.

## Rationale
*   A single mutable `balance` column is prone to race conditions.
*   `credit_transactions` will record `amount` (+ or -).
*   Searches will use PostgreSQL `SELECT SUM(amount) ... FOR UPDATE` or explicit balance materialization with row locks to guarantee no double spending.
