# =============================================
# ShortsCraft v2 — GitHub Publisher
# Run this in PowerShell inside the project folder
# =============================================

Write-Host ""
Write-Host "🚀 ShortsCraft v2 — GitHub Publisher" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 1. Get credentials
$username = Read-Host "Enter your GitHub username"
$token    = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
$plainToken = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
)
$repoName = "ShortsCraft-v2"

Write-Host ""
Write-Host "📦 Creating GitHub repository: $username/$repoName ..." -ForegroundColor Yellow

# 2. Create repo via GitHub API
$headers = @{
    Authorization = "Bearer $plainToken"
    Accept        = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}
$body = @{
    name        = $repoName
    description = "ShortsCraft 2.0 — Auto-generate YouTube Shorts with unique Picsum photo backgrounds per segment"
    private     = $false
    auto_init   = $false
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.github.com/user/repos" `
        -Method POST -Headers $headers -Body $body -ContentType "application/json"
    Write-Host "✅ Repo created: $($response.html_url)" -ForegroundColor Green
} catch {
    $errMsg = $_.ErrorDetails.Message | ConvertFrom-Json
    if ($errMsg.errors[0].message -like "*already exists*") {
        Write-Host "ℹ️  Repo already exists — continuing with push..." -ForegroundColor Cyan
    } else {
        Write-Host "❌ Failed to create repo: $($errMsg.message)" -ForegroundColor Red
        exit 1
    }
}

# 3. Set remote and push
$remoteUrl = "https://${username}:${plainToken}@github.com/$username/$repoName.git"

git remote remove origin 2>$null
git remote add origin $remoteUrl
git branch -M main

Write-Host ""
Write-Host "⬆️  Pushing code to GitHub..." -ForegroundColor Yellow
git push -u origin main --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Code pushed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Push failed. Check your token permissions (needs 'repo' scope)." -ForegroundColor Red
    exit 1
}

# 4. Enable GitHub Pages via API
Write-Host ""
Write-Host "🌐 Enabling GitHub Pages..." -ForegroundColor Yellow

$pagesBody = @{
    source = @{
        branch = "main"
        path   = "/"
    }
} | ConvertTo-Json

try {
    $pagesResp = Invoke-RestMethod `
        -Uri "https://api.github.com/repos/$username/$repoName/pages" `
        -Method POST -Headers $headers -Body $pagesBody -ContentType "application/json"
    Write-Host "✅ GitHub Pages enabled!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 Your site will be live in ~2 minutes at:" -ForegroundColor Cyan
    Write-Host "   https://$username.github.io/$repoName/" -ForegroundColor White
} catch {
    $errMsg = $_.ErrorDetails.Message | ConvertFrom-Json
    Write-Host "⚠️  Pages: $($errMsg.message)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "👉 Enable manually: https://github.com/$username/$repoName/settings/pages" -ForegroundColor Cyan
    Write-Host "   Source → main branch → /(root) → Save" -ForegroundColor White
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Repo  : https://github.com/$username/$repoName" -ForegroundColor White
Write-Host "Site  : https://$username.github.io/$repoName/" -ForegroundColor White
Write-Host "======================================" -ForegroundColor Cyan
