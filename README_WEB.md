# Social Media Listener - Web Interface

Modern web-based management interface for the social-spy monitoring tool.

## Features

- **Real-time Dashboard** - View stats, charts, and platform distribution
- **Post Management** - Browse, filter, and search social media posts
- **Monitoring Control** - Start/stop continuous monitoring via web UI
- **Manual Entries** - Add posts manually through a web form
- **RESTful API** - Full backend API with auto-generated documentation
- **Docker Deployment** - Easy deployment to any server

## Quick Start

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
nano .env

# Start the backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- API: http://localhost:8000/api
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

### 2. Frontend Setup

```bash
# Install Node.js dependencies
cd frontend
npm install

# Copy environment template
cp .env.example .env

# Start development server
npm run dev
```

Frontend will be available at http://localhost:5173

## Docker Deployment

Deploy the entire stack with Docker Compose:

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

## API Endpoints

### Monitoring
- `GET /api/monitoring/status` - Get monitoring status
- `POST /api/monitoring/start` - Start monitoring
- `POST /api/monitoring/stop` - Stop monitoring
- `POST /api/monitoring/fetch` - Manual fetch

### Posts
- `GET /api/posts` - Get posts with filters
- `GET /api/posts/stats` - Get statistics
- `GET /api/posts/recent` - Get recent posts

### Configuration
- `GET /api/config` - Get configuration
- `PUT /api/config/keywords` - Update keywords
- `PUT /api/config/channels/youtube` - Update YouTube channels

### Manual Entries
- `GET /api/manual` - Get all manual entries
- `POST /api/manual` - Create entry
- `DELETE /api/manual/{id}` - Delete entry

### Reports
- `POST /api/reports/dashboard` - Generate HTML dashboard
- `POST /api/reports/trends` - Generate trend report
- `GET /api/reports/dashboard/data` - Get dashboard data as JSON

## Architecture

```
social-spy/
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI app
│   ├── config.py        # Settings
│   ├── models/          # Pydantic schemas
│   ├── routers/         # API routes
│   ├── services/        # Business logic
│   └── middleware/      # CORS, etc.
├── frontend/            # React frontend
│   ├── src/
│   │   ├── api/        # API client
│   │   ├── components/ # React components
│   │   └── hooks/      # Custom hooks
│   └── package.json
├── docker/              # Docker files
└── docker-compose.yml   # Orchestration
```

## Environment Variables

### Backend (.env)
```
GROK_API_KEY=your_key_here
TWITTER_BEARER_TOKEN=your_token
META_ACCESS_TOKEN=your_token
LINKEDIN_ACCESS_TOKEN=your_token
CHECK_INTERVAL=30
MAX_POSTS_PER_PLATFORM=500
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

## CLI Still Works!

The original CLI functionality is preserved:

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

Both CLI and web interface can read/write the same data files.

## Development

### Backend Development
```bash
# Run with auto-reload
cd backend
uvicorn main:app --reload

# Run tests (when implemented)
pytest
```

### Frontend Development
```bash
cd frontend
npm run dev          # Development server
npm run build        # Production build
npm run lint         # Lint code
```

## Production Deployment

1. **Update environment files**
   - Set production API keys in `.env`
   - Set production API URL in `frontend/.env`

2. **Build and deploy with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Configure reverse proxy (optional)**
   - Use Nginx or Caddy for HTTPS
   - Point domain to frontend container

4. **Monitor logs**
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

## Troubleshooting

### Backend won't start
- Check Python version (3.12+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check `.env` file exists and has valid values

### Frontend won't connect to backend
- Verify backend is running on port 8000
- Check `VITE_API_URL` in `frontend/.env`
- Check CORS settings in `backend/config.py`

### Docker containers fail
- Check port 3000 and 8000 are available
- Verify Docker and Docker Compose installed
- Check `docker-compose logs` for errors

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Same license as the parent social-spy project.
