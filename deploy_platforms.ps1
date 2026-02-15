# NinjaQuant API - Multi-Platform Deployment Script
# For Windows PowerShell

Write-Host "🚀 NinjaQuant API - Platform Deployment" -ForegroundColor Cyan
Write-Host ""

Write-Host "Choose your deployment platform:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Deta Space    (Forever FREE, No card required) ⭐" -ForegroundColor Green
Write-Host "2. Fly.io        (Generous FREE tier, Card required)" -ForegroundColor Green
Write-Host "3. Render        (750hr/month FREE, after trial need card)" -ForegroundColor Yellow
Write-Host "4. Railway       (Limited FREE credit)" -ForegroundColor Yellow
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🛸 Deploying to Deta Space..." -ForegroundColor Cyan
        Write-Host ""
        
        # Check if Space CLI is installed
        $spaceInstalled = Get-Command space -ErrorAction SilentlyContinue
        
        if (-not $spaceInstalled) {
            Write-Host "Installing Deta Space CLI..." -ForegroundColor Yellow
            iwr https://deta.space/assets/space-cli.ps1 -useb | iex
            
            Write-Host ""
            Write-Host "✅ Space CLI installed!" -ForegroundColor Green
            Write-Host ""
        }
        
        # Check if logged in
        Write-Host "Checking login status..." -ForegroundColor Yellow
        $loginCheck = space whoami 2>&1
        
        if ($loginCheck -match "not logged in" -or $loginCheck -match "error") {
            Write-Host ""
            Write-Host "Please login to Deta Space:" -ForegroundColor Yellow
            space login
            Write-Host ""
        }
        
        Write-Host "🚀 Deploying to Deta Space..." -ForegroundColor Cyan
        
        # Check if already initialized
        $detaExists = Test-Path ".space"
        
        if (-not $detaExists) {
            Write-Host ""
            Write-Host "Initializing new Space project..." -ForegroundColor Yellow
            space new
        }
        
        Write-Host ""
        Write-Host "Pushing code to Space..." -ForegroundColor Yellow
        space push
        
        Write-Host ""
        Write-Host "✅ Deployment complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Get your URL with:" -ForegroundColor Cyan
        Write-Host "  space open" -ForegroundColor White
        Write-Host ""
    }
    
    "2" {
        Write-Host ""
        Write-Host "🪁 Deploying to Fly.io..." -ForegroundColor Cyan
        Write-Host ""
        
        # Check if Fly CLI is installed
        $flyInstalled = Get-Command flyctl -ErrorAction SilentlyContinue
        
        if (-not $flyInstalled) {
            Write-Host "Installing Fly CLI..." -ForegroundColor Yellow
            iwr https://fly.io/install.ps1 -useb | iex
            
            Write-Host ""
            Write-Host "✅ Fly CLI installed!" -ForegroundColor Green
            Write-Host "⚠️  Please restart PowerShell and run this script again." -ForegroundColor Yellow
            Write-Host ""
            pause
            exit
        }
        
        # Check if logged in
        Write-Host "Checking login status..." -ForegroundColor Yellow
        $flyAuth = fly auth whoami 2>&1
        
        if ($flyAuth -match "not logged in" -or $flyAuth -match "error") {
            Write-Host ""
            Write-Host "Please login to Fly.io:" -ForegroundColor Yellow
            fly auth login
            Write-Host ""
        }
        
        Write-Host "🚀 Deploying to Fly.io..." -ForegroundColor Cyan
        
        # Check if already initialized
        $flyExists = Test-Path "fly.toml"
        
        if ($flyExists) {
            Write-Host ""
            Write-Host "fly.toml found. Deploying..." -ForegroundColor Yellow
            fly deploy
        } else {
            Write-Host ""
            Write-Host "Launching new Fly app..." -ForegroundColor Yellow
            fly launch
        }
        
        Write-Host ""
        Write-Host "✅ Deployment complete!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your API is live at:" -ForegroundColor Cyan
        fly status
        Write-Host ""
    }
    
    "3" {
        Write-Host ""
        Write-Host "🌊 Render Deployment Instructions:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Push your code to GitHub:" -ForegroundColor Yellow
        Write-Host "   git add -A" -ForegroundColor White
        Write-Host "   git commit -m 'Deploy to Render'" -ForegroundColor White
        Write-Host "   git push" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Go to: https://render.com" -ForegroundColor Yellow
        Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor Yellow
        Write-Host "4. Connect your GitHub repository" -ForegroundColor Yellow
        Write-Host "5. Settings:" -ForegroundColor Yellow
        Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor White
        Write-Host "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port `$PORT" -ForegroundColor White
        Write-Host "   - Add env vars: USE_REAL_DATA=true, INJECTIVE_NETWORK=mainnet" -ForegroundColor White
        Write-Host ""
        Write-Host "✅ runtime.txt is already configured for Python 3.11" -ForegroundColor Green
        Write-Host ""
    }
    
    "4" {
        Write-Host ""
        Write-Host "🚂 Railway Deployment Instructions:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Push your code to GitHub:" -ForegroundColor Yellow
        Write-Host "   git add -A" -ForegroundColor White
        Write-Host "   git commit -m 'Deploy to Railway'" -ForegroundColor White
        Write-Host "   git push" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Go to: https://railway.app" -ForegroundColor Yellow
        Write-Host "3. Click 'New Project' → 'Deploy from GitHub repo'" -ForegroundColor Yellow
        Write-Host "4. Select your repository" -ForegroundColor Yellow
        Write-Host "5. Railway will auto-detect and deploy!" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "✅ railway.json and nixpacks.toml are configured" -ForegroundColor Green
        Write-Host ""
    }
    
    default {
        Write-Host ""
        Write-Host "❌ Invalid choice. Please run again and select 1-4." -ForegroundColor Red
        Write-Host ""
    }
}

Write-Host ""
Write-Host "For more details, see FREE_HOSTING.md" -ForegroundColor Cyan
Write-Host ""
pause
