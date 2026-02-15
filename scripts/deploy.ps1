# NinjaQuant - Quick Docker Deployment Script (Windows)

Write-Host "🚀 NinjaQuant - Docker Deployment" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Build the image
Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
docker build -t ninjaquant-api .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker image built successfully" -ForegroundColor Green
Write-Host ""

# Stop and remove existing container if running
Write-Host "🧹 Cleaning up old containers..." -ForegroundColor Yellow
docker stop ninjaquant 2>$null
docker rm ninjaquant 2>$null

Write-Host "✅ Cleanup complete" -ForegroundColor Green
Write-Host ""

# Run the container
Write-Host "🚀 Starting NinjaQuant API..." -ForegroundColor Yellow
docker run -d `
  -p 8000:8000 `
  -e USE_REAL_DATA=true `
  -e INJECTIVE_NETWORK=mainnet `
  --name ninjaquant `
  ninjaquant-api

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start container" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Container started successfully" -ForegroundColor Green
Write-Host ""

# Wait for container to be healthy
Write-Host "⏳ Waiting for API to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if API is responding
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ API is responding!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🎉 Deployment successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 API URL: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "📊 View logs: docker logs -f ninjaquant" -ForegroundColor Cyan
        Write-Host "🛑 Stop API: docker stop ninjaquant" -ForegroundColor Cyan
        Write-Host ""
    }
} catch {
    Write-Host "⚠️  API is not responding yet" -ForegroundColor Yellow
    Write-Host "   Check logs with: docker logs -f ninjaquant" -ForegroundColor Yellow
}

# Show logs
Write-Host "📋 Recent logs:" -ForegroundColor Yellow
Write-Host "===============" -ForegroundColor Yellow
docker logs --tail 20 ninjaquant
