#!/bin/bash
# Deployment Wizard

echo "========================================="
echo "   Scalable Search Platform Installer"
echo "========================================="

# Disk space check
FREE_SPACE=$(df -m . | awk 'NR==2 {print $4}')
if [ "$FREE_SPACE" -lt 3500 ]; then
    echo "WARNING: You have less than 3500MB of free disk space in the current directory."
    echo "Docker build might fail with 'no space left on device'."
    read -p "Do you want to continue anyway? (y/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        kill -INT $$
    fi
fi

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

# Generate .env if missing
if [ ! -f .env ]; then
    cp .env.example .env
fi

if [ -n "$BOT_TOKEN" ]; then
    sed -i "s/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=$BOT_TOKEN/" .env
fi
if [ -n "$ADMIN_IDS" ]; then
    sed -i "s/ADMIN_IDS=.*/ADMIN_IDS=$ADMIN_IDS/" .env
fi

echo ""
echo "Configuration saved to .env"

# Check for docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install docker and docker compose plugin first."
    kill -INT $$
fi

# Detect docker-compose command
DOCKER_COMPOSE_CMD=""
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "Docker Compose is not available. Please install docker-compose-plugin."
    kill -INT $$
fi

echo "Cleaning up old containers..."
$DOCKER_COMPOSE_CMD --profile app down || true

echo "Starting infrastructure services using Docker Compose..."
$DOCKER_COMPOSE_CMD up -d --force-recreate db redis opensearch minio

echo "Waiting for DB to initialize..."
sleep 15

echo "Building containers (this might take a few minutes)..."
$DOCKER_COMPOSE_CMD --profile app build

echo "Running migrations..."
echo "Running migrations via docker..."
$DOCKER_COMPOSE_CMD run --rm api alembic upgrade head || echo "WARNING: Migrations failed. You may need to investigate via logs."

if [ "$TOPOLOGY" == "1" ]; then
    echo "Starting App (Bot, API) and Worker services..."
    $DOCKER_COMPOSE_CMD --profile app up -d --force-recreate
    echo "Done! The platform is now running in All-in-One mode."
    echo "Use '$DOCKER_COMPOSE_CMD logs -f' to view logs."
else
    echo "For Multi-Server topologies, please refer to docs/ROADMAP.md and docs/architecture/TOPOLOGY_AND_SCALING.md to configure Ansible."
fi
