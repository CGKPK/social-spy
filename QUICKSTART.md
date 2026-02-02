# Quick Start Guide

Get the Social Media Listener web interface running in 5 minutes.

## Prerequisites

- Python 3.12+
- Node.js 18+
- npm or yarn

## Option 1: Development Mode (Recommended for Testing)

### Step 1: Backend Setup

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API keys (optional for testing)
nano .env

# Start backend (includes dependency installation)
chmod +x start_backend.sh
./start_backend.sh
```

Backend will start on http://localhost:8000

### Step 2: Frontend Setup (New Terminal)

```bash
# Start frontend (includes dependency installation)
chmod +x start_frontend.sh
./start_frontend.sh
```

Frontend will start on http://localhost:5173

### Step 3: Access the Application

Open your browser:
- **Web UI**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/api/health

## Option 2: Docker (Recommended for Production)

### Step 1: Setup Environment

```bash
# Create .env file
cp .env.example .env

# Edit and add your API keys
nano .env
```

### Step 2: Build and Run

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 3: Access

- **Web UI + API**: http://localhost:3000
- **API Docs**: http://localhost:3000/docs

### Stop Services

```bash
docker-compose down
```

## First Time Using the Interface

### 1. Check Dashboard
- Navigate to Dashboard page
- View statistics (will be empty initially)

### 2. Run First Fetch
- Go to Monitoring page
- Click "Fetch Now" button
- Wait for data to load

Or use the CLI:
```bash
python listener.py
```

### 3. View Posts
- Navigate to Posts page
- Filter by platform
- Browse collected posts

### 4. Add Manual Entry
- Go to Add Entry page
- Fill in the form
- Submit

### 5. Start Continuous Monitoring
- Go to Monitoring page
- Set interval (e.g., 30 minutes)
- Click "Start Monitoring"
- Monitoring will run in background

## Testing Everything Works

```bash
# Test backend
curl http://localhost:8000/api/health

# Test posts endpoint
curl http://localhost:8000/api/posts

# Test stats
curl http://localhost:8000/api/posts/stats
```

## Common Issues

### Port Already in Use

Backend (8000):
```bash
# Find process
lsof -i :8000

# Kill if needed
kill -9 <PID>
```

Frontend (5173):
```bash
# Find process
lsof -i :5173

# Kill if needed
kill -9 <PID>
```

### Module Not Found (Backend)

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies Not Installing (Frontend)

```bash
cd frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### API Not Connecting

Check frontend/.env has correct API URL:
```
VITE_API_URL=http://localhost:8000/api
```

### CORS Errors

Check .env has frontend URL in ALLOWED_ORIGINS:
```
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## CLI Still Works!

The original CLI is unchanged:

```bash
# Single fetch
python listener.py

# Continuous monitoring
python listener.py --watch --interval 30

# Add manual entry
python listener.py --add

# Generate dashboard only
python listener.py --dashboard
```

## Next Steps

1. **Configure API Keys**
   - Edit .env file
   - Add your social media API keys
   - Restart backend

2. **Customize Keywords**
   - Go to Configuration page (when implemented)
   - Or edit config.py directly
   - Restart services

3. **Schedule Monitoring**
   - Use web UI to start monitoring
   - Or use cron for CLI:
     ```bash
     # Edit crontab
     crontab -e

     # Add line (runs every 30 minutes)
     */30 * * * * cd /path/to/social-spy && python listener.py
     ```

4. **Deploy to Production**
   - See README_WEB.md for deployment guide
   - Use docker-compose for easy deployment
   - Configure reverse proxy (Nginx/Caddy) for HTTPS

## Getting Help

- **Backend Issues**: Check backend logs in terminal
- **Frontend Issues**: Check browser console (F12)
- **Docker Issues**: Check logs with `docker-compose logs`
- **API Documentation**: http://localhost:8000/docs
- **Full Documentation**: See README_WEB.md
- **Testing Guide**: See TESTING.md

## File Locations

- **Data**: `social_data.json`
- **Manual Entries**: `manual_entries.json`
- **Configuration**: `config.py` and `.env`
- **Dashboard**: `dashboard.html` (generated)
- **Trends**: `trend_report.md` (generated)

## Default Ports

- Backend API: 8000
- Frontend Dev: 5173
- Frontend Prod (Docker): 3000

## Environment Variables

### Backend (.env)
```bash
GROK_API_KEY=          # xAI Grok API key
TWITTER_BEARER_TOKEN=  # Twitter API token
META_ACCESS_TOKEN=     # Meta Graph API token
LINKEDIN_ACCESS_TOKEN= # LinkedIn API token
CHECK_INTERVAL=30      # Default monitoring interval
MAX_POSTS_PER_PLATFORM=500  # Posts to keep per platform
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (frontend/.env)
```bash
VITE_API_URL=http://localhost:8000/api
```

## Quick Commands Reference

```bash
# Development
./start_backend.sh          # Start backend
./start_frontend.sh         # Start frontend

# Docker
docker-compose up -d        # Start all services
docker-compose down         # Stop all services
docker-compose logs -f      # View logs
docker-compose restart      # Restart services

# CLI
python listener.py          # Run once
python listener.py --watch  # Continuous mode
python listener.py --add    # Add entry

# Testing
curl http://localhost:8000/api/health  # Test backend
open http://localhost:5173             # Test frontend
```

That's it! You should now have a fully functional web interface for your social media listener.
