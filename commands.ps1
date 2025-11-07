# Agent-on-Call - PowerShell Commands
# Run these commands from the project root directory

Write-Host "Agent-on-Call - Available Commands" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Setup & Start:" -ForegroundColor Yellow
Write-Host "  .\commands.ps1 setup          - Initial setup with Docker" -ForegroundColor White
Write-Host "  .\commands.ps1 start          - Start all services" -ForegroundColor White
Write-Host "  .\commands.ps1 stop           - Stop all services" -ForegroundColor White
Write-Host "  .\commands.ps1 restart        - Restart all services" -ForegroundColor White
Write-Host ""
Write-Host "Development:" -ForegroundColor Yellow
Write-Host "  .\commands.ps1 logs           - View all logs" -ForegroundColor White
Write-Host "  .\commands.ps1 logs-backend   - View backend logs" -ForegroundColor White
Write-Host "  .\commands.ps1 logs-frontend  - View frontend logs" -ForegroundColor White
Write-Host "  .\commands.ps1 build          - Rebuild containers" -ForegroundColor White
Write-Host ""
Write-Host "Testing:" -ForegroundColor Yellow
Write-Host "  .\commands.ps1 test           - Run backend tests" -ForegroundColor White
Write-Host "  .\commands.ps1 test-coverage  - Run tests with coverage" -ForegroundColor White
Write-Host ""
Write-Host "Database:" -ForegroundColor Yellow
Write-Host "  .\commands.ps1 db-shell       - Open MongoDB shell" -ForegroundColor White
Write-Host "  .\commands.ps1 db-reset       - Reset database" -ForegroundColor White
Write-Host ""
Write-Host "Maintenance:" -ForegroundColor Yellow
Write-Host "  .\commands.ps1 clean          - Stop and remove containers" -ForegroundColor White
Write-Host "  .\commands.ps1 clean-all      - Deep clean (includes volumes)" -ForegroundColor White
Write-Host "  .\commands.ps1 status         - Show service status" -ForegroundColor White
Write-Host ""

param(
    [Parameter(Position=0)]
    [string]$Command
)

function Show-Help {
    Write-Host "Usage: .\commands.ps1 <command>" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Run without arguments to see all available commands" -ForegroundColor Gray
}

switch ($Command) {
    "setup" {
        Write-Host "🚀 Setting up Agent-on-Call..." -ForegroundColor Cyan
        if (-not (Test-Path ".env")) {
            Copy-Item ".env.example" ".env"
            Write-Host "✅ Created .env file" -ForegroundColor Green
        }
        docker-compose up --build -d
        Write-Host "✅ Setup complete!" -ForegroundColor Green
        Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
        Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
        Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    
    "start" {
        Write-Host "▶️  Starting services..." -ForegroundColor Cyan
        docker-compose up -d
        Write-Host "✅ Services started!" -ForegroundColor Green
    }
    
    "stop" {
        Write-Host "⏹️  Stopping services..." -ForegroundColor Cyan
        docker-compose down
        Write-Host "✅ Services stopped!" -ForegroundColor Green
    }
    
    "restart" {
        Write-Host "🔄 Restarting services..." -ForegroundColor Cyan
        docker-compose restart
        Write-Host "✅ Services restarted!" -ForegroundColor Green
    }
    
    "logs" {
        Write-Host "📋 Viewing all logs (Ctrl+C to exit)..." -ForegroundColor Cyan
        docker-compose logs -f
    }
    
    "logs-backend" {
        Write-Host "📋 Viewing backend logs (Ctrl+C to exit)..." -ForegroundColor Cyan
        docker-compose logs -f backend
    }
    
    "logs-frontend" {
        Write-Host "📋 Viewing frontend logs (Ctrl+C to exit)..." -ForegroundColor Cyan
        docker-compose logs -f frontend
    }
    
    "build" {
        Write-Host "🔨 Rebuilding containers..." -ForegroundColor Cyan
        docker-compose build --no-cache
        docker-compose up -d
        Write-Host "✅ Build complete!" -ForegroundColor Green
    }
    
    "test" {
        Write-Host "🧪 Running tests..." -ForegroundColor Cyan
        docker-compose exec backend pytest tests/ -v
    }
    
    "test-coverage" {
        Write-Host "🧪 Running tests with coverage..." -ForegroundColor Cyan
        docker-compose exec backend pytest tests/ --cov=. --cov-report=term-missing
    }
    
    "db-shell" {
        Write-Host "🗄️  Opening MongoDB shell..." -ForegroundColor Cyan
        docker-compose exec mongodb mongosh
    }
    
    "db-reset" {
        Write-Host "⚠️  Resetting database..." -ForegroundColor Yellow
        $confirm = Read-Host "Are you sure? This will delete all data (y/n)"
        if ($confirm -eq "y") {
            docker-compose down -v
            docker-compose up -d
            Write-Host "✅ Database reset!" -ForegroundColor Green
        } else {
            Write-Host "❌ Cancelled" -ForegroundColor Red
        }
    }
    
    "clean" {
        Write-Host "🧹 Cleaning up..." -ForegroundColor Cyan
        docker-compose down
        Write-Host "✅ Cleanup complete!" -ForegroundColor Green
    }
    
    "clean-all" {
        Write-Host "🧹 Deep cleaning..." -ForegroundColor Cyan
        $confirm = Read-Host "This will remove all containers, volumes, and images. Continue? (y/n)"
        if ($confirm -eq "y") {
            docker-compose down -v --rmi all
            Write-Host "✅ Deep clean complete!" -ForegroundColor Green
        } else {
            Write-Host "❌ Cancelled" -ForegroundColor Red
        }
    }
    
    "status" {
        Write-Host "📊 Service Status:" -ForegroundColor Cyan
        docker-compose ps
        Write-Host ""
        Write-Host "📊 Resource Usage:" -ForegroundColor Cyan
        docker stats --no-stream
    }
    
    "open" {
        Write-Host "🌐 Opening application..." -ForegroundColor Cyan
        Start-Process "http://localhost:5173"
        Start-Process "http://localhost:8000/docs"
    }
    
    "dev-backend" {
        Write-Host "💻 Starting backend in development mode..." -ForegroundColor Cyan
        cd backend
        if (-not (Test-Path "venv")) {
            python -m venv venv
        }
        .\venv\Scripts\activate
        pip install -r requirements.txt
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
    }
    
    "dev-frontend" {
        Write-Host "💻 Starting frontend in development mode..." -ForegroundColor Cyan
        cd frontend
        npm install
        npm run dev
    }
    
    default {
        if ($Command) {
            Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
            Write-Host ""
        }
        # Show help by displaying the header again (it's already shown)
    }
}
