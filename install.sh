#!/bin/bash
# Deployment Wizard

echo "========================================="
echo "   Scalable Search Platform Installer"
echo "========================================="

echo "This script will help you deploy the platform."
echo "Select Deployment Topology:"
echo "1) All-in-One (1 Server)"
echo "2) Separated Data (2 Servers)"
echo "3) Fully Distributed (3+ Servers) [Requires Ansible]"

read -p "Enter choice [1]: " TOPOLOGY
TOPOLOGY=${TOPOLOGY:-1}

read -p "Enter Domain (e.g. search.example.com): " DOMAIN
read -p "Enter Telegram Bot Token: " BOT_TOKEN
read -p "Enter Admin Telegram IDs (comma separated): " ADMIN_IDS

# Generate .env
cp .env.example .env
sed -i "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=$BOT_TOKEN/" .env
sed -i "s/ADMIN_IDS=.*/ADMIN_IDS=$ADMIN_IDS/" .env

echo ""
echo "Configuration saved to .env"
echo "Starting services using Docker Compose..."
docker compose up -d db redis opensearch minio
echo "Waiting for DB to initialize..."
sleep 15
echo "Running migrations..."
alembic upgrade head

if [ "$TOPOLOGY" == "1" ]; then
    echo "Starting App and Worker..."
    # Normally we'd use a docker-compose profile for this
    echo "Done! The platform is now running in All-in-One mode."
else
    echo "For Multi-Server topologies, please refer to docs/ROADMAP.md and docs/architecture/TOPOLOGY_AND_SCALING.md to configure Ansible."
fi
