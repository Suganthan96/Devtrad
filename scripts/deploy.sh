#!/bin/bash

# NinjaQuant - Quick Docker Deployment Script

echo "🚀 NinjaQuant - Docker Deployment"
echo "=================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker is installed"
echo ""

# Build the image
echo "📦 Building Docker image..."
docker build -t ninjaquant-api .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"
echo ""

# Stop and remove existing container if running
echo "🧹 Cleaning up old containers..."
docker stop ninjaquant 2>/dev/null
docker rm ninjaquant 2>/dev/null

echo "✅ Cleanup complete"
echo ""

# Run the container
echo "🚀 Starting NinjaQuant API..."
docker run -d \
  -p 8000:8000 \
  -e USE_REAL_DATA=true \
  -e INJECTIVE_NETWORK=mainnet \
  --name ninjaquant \
  ninjaquant-api

if [ $? -ne 0 ]; then
    echo "❌ Failed to start container"
    exit 1
fi

echo "✅ Container started successfully"
echo ""

# Wait for container to be healthy
echo "⏳ Waiting for API to be ready..."
sleep 5

# Check if API is responding
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)

if [ "$response" == "200" ]; then
    echo "✅ API is responding!"
    echo ""
    echo "🎉 Deployment successful!"
    echo ""
    echo "📍 API URL: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "📊 View logs: docker logs -f ninjaquant"
    echo "🛑 Stop API: docker stop ninjaquant"
    echo ""
else
    echo "⚠️  API is not responding yet (HTTP $response)"
    echo "   Check logs with: docker logs -f ninjaquant"
fi

# Show logs
echo "📋 Recent logs:"
echo "==============="
docker logs --tail 20 ninjaquant
