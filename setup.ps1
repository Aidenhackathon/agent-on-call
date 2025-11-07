# Agent-on-Call Setup Script
# This script helps set up the project for first-time use

Write-Host "🚀 Agent-on-Call Setup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} else {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
Write-Host "Checking Docker Compose..." -ForegroundColor Yellow
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker Compose is available" -ForegroundColor Green
} else {
    Write-Host "❌ Docker Compose is not available." -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Setting up environment variables..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Please edit .env and add your Gemini API key!" -ForegroundColor Yellow
    Write-Host "   Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
    Write-Host ""
    
    $response = Read-Host "Do you want to enter your Gemini API key now? (y/n)"
    if ($response -eq "y") {
        $apiKey = Read-Host "Enter your Gemini API key"
        if ($apiKey) {
            (Get-Content ".env") -replace 'GEMINI_API_KEY=your_gemini_api_key_here', "GEMINI_API_KEY=$apiKey" | Set-Content ".env"
            Write-Host "✅ API key saved" -ForegroundColor Green
        }
    } else {
        Write-Host "⚠️  Mock AI mode will be used. Set USE_MOCK_AI=false after adding API key." -ForegroundColor Yellow
        (Get-Content ".env") -replace 'USE_MOCK_AI=false', 'USE_MOCK_AI=true' | Set-Content ".env"
    }
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting Docker containers..." -ForegroundColor Yellow
docker-compose up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Access your application:" -ForegroundColor Cyan
    Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor White
    Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
    Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 View logs with: docker-compose logs -f" -ForegroundColor Cyan
    Write-Host "🛑 Stop with: docker-compose down" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Setup failed. Check the errors above." -ForegroundColor Red
}
