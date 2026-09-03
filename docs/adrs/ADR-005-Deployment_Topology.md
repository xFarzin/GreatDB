# ADR 005: Deployment Topology

## Context
The system must be easily installable via a wizard and support seamless migration from a 2-server to a 3+ server setup.

## Decision
The core application will be broken into Docker Compose profiles or independent `docker-compose.yml` components. Deployment configuration will be driven by an Ansible playbook wrapped in a bash `deploy.sh` wizard.

## Rationale
*   Ansible is idempotent and perfect for "add server" wizard flows.
*   Stateless app containers allow workers and APIs to be shifted across hardware seamlessly.
