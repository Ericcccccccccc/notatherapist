#!/bin/bash

set -e

# Configuration
REMOTE_HOST="170.9.233.1"
SSH_KEY="$HOME/Documents/tech/notatherapist/oracle-ssh.key"

echo "🚀 Deploying to notatherapist.com..."

echo "📦 Building Docker images..."
echo "  - Building frontend..."
docker build -t notatherapist-frontend ./frontend
echo "  - Building backend..."
docker build -t notatherapist-backend ./backend

echo "💾 Saving Docker images..."
docker save notatherapist-frontend notatherapist-backend | gzip > notatherapist-images.tar.gz

echo "📤 Uploading to server..."
scp -i "${SSH_KEY}" notatherapist-images.tar.gz ubuntu@${REMOTE_HOST}:/tmp/

# Check if .env exists locally
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found locally"
    echo "   Please create .env from .env.example before deployment"
    exit 1
fi

# Upload configuration files
scp -i "${SSH_KEY}" docker-compose.yml ubuntu@${REMOTE_HOST}:~/
scp -i "${SSH_KEY}" .env ubuntu@${REMOTE_HOST}:~/

echo "🔧 Deploying on server..."
ssh -i "${SSH_KEY}" ubuntu@${REMOTE_HOST} << EOF
    set -e
    
    # Install Docker if not present
    if ! command -v docker &> /dev/null; then
        echo "Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker \$USER
        rm get-docker.sh
    fi
    
    # Install Docker Compose if not present
    if ! command -v docker-compose &> /dev/null; then
        echo "Installing Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    # Load Docker images
    echo "Loading Docker images..."
    docker load < /tmp/notatherapist-images.tar.gz
    rm /tmp/notatherapist-images.tar.gz
    
    # Stop ALL existing containers and remove orphans
    docker-compose down --remove-orphans 2>/dev/null || true
    
    # Extra cleanup - stop any container using port 5004
    docker ps -q --filter "publish=5004" | xargs -r docker stop
    docker ps -aq --filter "publish=5004" | xargs -r docker rm
    
    # Start the application
    echo "Starting application..."
    docker-compose up -d
    
    # Open firewall ports (Oracle Cloud specific)
    sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
    sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
    sudo netfilter-persistent save 2>/dev/null || true
    
    docker ps
EOF

rm -f notatherapist-images.tar.gz

echo "✅ Deployed to https://notatherapist.com"