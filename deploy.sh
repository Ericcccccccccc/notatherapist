#!/bin/bash

set -e

# Configuration
REMOTE_HOST="170.9.233.1"
SSH_KEY="$HOME/Documents/tech/notatherapist/oracle-ssh.key"

echo "🚀 Deploying to notatherapist.com..."

echo "📦 Building Docker image..."
docker build -t notatherapist-frontend ./frontend

echo "💾 Saving Docker image..."
docker save notatherapist-frontend | gzip > notatherapist-frontend.tar.gz

echo "📤 Uploading to server..."
scp -i "${SSH_KEY}" notatherapist-frontend.tar.gz ubuntu@${REMOTE_HOST}:/tmp/
scp -i "${SSH_KEY}" docker-compose.yml ubuntu@${REMOTE_HOST}:~/

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
    
    # Load Docker image
    echo "Loading Docker image..."
    docker load < /tmp/notatherapist-frontend.tar.gz
    rm /tmp/notatherapist-frontend.tar.gz
    
    # Stop existing container if running
    docker-compose down 2>/dev/null || true
    
    # Start the application
    echo "Starting application..."
    docker-compose up -d
    
    # Open firewall ports (Oracle Cloud specific)
    sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
    sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
    sudo netfilter-persistent save 2>/dev/null || true
    
    docker ps
EOF

rm -f notatherapist-frontend.tar.gz

echo "✅ Deployed to https://notatherapist.com"