# Deploy to Render - Full Fix Script
# This pushes the required config files to fix the Python 3.14 issue

Write-Host "[RENDER FIX] Fixing Render Deployment Issues" -ForegroundColor Cyan
Write-Host ""

Write-Host "Files created/updated:" -ForegroundColor Yellow
Write-Host "  - render.yaml (forces Python 3.11, Rust config)" -ForegroundColor Green
Write-Host "  - .python-version (Python 3.11.0)" -ForegroundColor Green
Write-Host "  - runtime.txt (Python 3.11.0)" -ForegroundColor Green
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "[WARNING] Git not initialized. Initializing..." -ForegroundColor Yellow
    git init
    Write-Host ""
}

# Check current status
Write-Host "[GIT] Current git status:" -ForegroundColor Cyan
git status -s
Write-Host ""

# Stage the new files
Write-Host "[STAGING] Staging Render configuration files..." -ForegroundColor Yellow
git add render.yaml
git add .python-version
git add runtime.txt
git add requirements.txt
git add Spacefile
git add fly.toml
git add FREE_HOSTING.md
git add deploy_platforms.ps1

Write-Host "[SUCCESS] Files staged" -ForegroundColor Green
Write-Host ""

# Show what will be committed
Write-Host "[FILES] Files to commit:" -ForegroundColor Cyan
git diff --staged --name-only
Write-Host ""

# Commit
$commitMsg = "Fix: Render deployment - Force Python 3.11, add render.yaml"
Write-Host "[COMMIT] Committing with message: $commitMsg" -ForegroundColor Yellow
git commit -m $commitMsg

if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] Commit failed or nothing to commit" -ForegroundColor Yellow
} else {
    Write-Host "[SUCCESS] Changes committed" -ForegroundColor Green
}
Write-Host ""

# Ask to push
Write-Host "[PUSH] Ready to push to GitHub?" -ForegroundColor Cyan
Write-Host ""
Write-Host "After pushing:" -ForegroundColor Yellow
Write-Host "  1. Go to render.com" -ForegroundColor White
Write-Host "  2. It will detect render.yaml automatically" -ForegroundColor White
Write-Host "  3. Deploy will use Python 3.11 (has pre-built pydantic wheels)" -ForegroundColor White
Write-Host ""

$push = Read-Host "Push now? (y/n)"

if ($push -eq "y" -or $push -eq "Y") {
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    
    # Check if remote exists
    $remoteCheck = git remote -v 2>&1
    
    if ($remoteCheck -match "origin") {
        git push
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "[SUCCESS] Successfully pushed to GitHub!" -ForegroundColor Green
            Write-Host ""
            Write-Host "[RENDER] Next steps for Render:" -ForegroundColor Cyan
            Write-Host "  1. Go to https://render.com/dashboard" -ForegroundColor White
            Write-Host "  2. Create new 'Web Service'" -ForegroundColor White
            Write-Host "  3. Connect your GitHub repo" -ForegroundColor White
            Write-Host "  4. Render will auto-detect render.yaml" -ForegroundColor White
            Write-Host "  5. Click 'Create Web Service'" -ForegroundColor White
            Write-Host ""
            Write-Host "render.yaml will force Python 3.11 (avoids Rust compilation)" -ForegroundColor Green
            Write-Host ""
        } else {
            Write-Host ""
            Write-Host "[ERROR] Push failed. Check your remote and try: git push" -ForegroundColor Red
            Write-Host ""
        }
    } else {
        Write-Host ""
        Write-Host "[WARNING] No remote 'origin' found." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Add GitHub remote first:" -ForegroundColor Cyan
        Write-Host '  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git' -ForegroundColor White
        Write-Host "  git push -u origin main" -ForegroundColor White
        Write-Host ""
    }
} else {
    Write-Host ""
    Write-Host "Push manually when ready:" -ForegroundColor Cyan
    Write-Host "  git push" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "Alternative: Use Deta Space (no card needed)" -ForegroundColor Cyan
Write-Host "  Run: .\deploy_platforms.ps1" -ForegroundColor White
Write-Host "  Choose option 1" -ForegroundColor White
Write-Host ""

pause
