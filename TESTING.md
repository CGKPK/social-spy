# Testing Guide

This guide covers testing both the backend API and frontend interface.

## Quick Start Testing

### 1. Backend Testing

```bash
# Start the backend
./start_backend.sh

# In another terminal, test the health endpoint
curl http://localhost:8000/api/health

# View API documentation
open http://localhost:8000/docs
```

#### Test Monitoring Endpoints

```bash
# Get monitoring status
curl http://localhost:8000/api/monitoring/status

# Start monitoring (30 minute interval)
curl -X POST http://localhost:8000/api/monitoring/start \
  -H "Content-Type: application/json" \
  -d '{"interval_minutes": 30}'

# Manual fetch
curl -X POST http://localhost:8000/api/monitoring/fetch

# Stop monitoring
curl -X POST http://localhost:8000/api/monitoring/stop
```

#### Test Posts Endpoints

```bash
# Get all posts
curl http://localhost:8000/api/posts

# Get posts with filters
curl "http://localhost:8000/api/posts?platform=youtube&limit=10"

# Get statistics
curl http://localhost:8000/api/posts/stats

# Get recent posts
curl "http://localhost:8000/api/posts/recent?days=7&limit=20"
```

#### Test Configuration Endpoints

```bash
# Get configuration
curl http://localhost:8000/api/config

# Update keywords
curl -X PUT http://localhost:8000/api/config/keywords \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["test", "keyword"]}'
```

#### Test Manual Entries

```bash
# Create manual entry
curl -X POST http://localhost:8000/api/manual \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "twitter",
    "text": "Test post from API",
    "author": "TestUser",
    "tags": ["test", "api"]
  }'

# Get all manual entries
curl http://localhost:8000/api/manual

# Delete entry (replace {id} with actual ID)
curl -X DELETE http://localhost:8000/api/manual/{id}
```

#### Test Reports

```bash
# Generate dashboard
curl -X POST http://localhost:8000/api/reports/dashboard

# Generate trends
curl -X POST http://localhost:8000/api/reports/trends

# Get dashboard data as JSON
curl http://localhost:8000/api/reports/dashboard/data
```

### 2. Frontend Testing

```bash
# Start the frontend
./start_frontend.sh

# Access in browser
open http://localhost:5173
```

#### Manual Testing Checklist

- [ ] Dashboard loads and shows statistics
- [ ] Platform distribution chart displays
- [ ] Posts page loads with list of posts
- [ ] Filtering by platform works
- [ ] Pagination works
- [ ] Monitoring control shows correct status
- [ ] Start/Stop monitoring buttons work
- [ ] Manual fetch button triggers fetch
- [ ] Manual entry form submits successfully
- [ ] Navigation between pages works

### 3. Docker Testing

```bash
# Build and start containers
docker-compose up -d

# Check logs
docker-compose logs -f

# Test frontend
curl http://localhost:3000

# Test backend API
curl http://localhost:3000/api/health

# Test API docs through proxy
open http://localhost:3000/docs

# Stop containers
docker-compose down
```

## Integration Testing

### Test CLI + Backend Interaction

1. Start the backend:
   ```bash
   ./start_backend.sh
   ```

2. In another terminal, run CLI:
   ```bash
   python listener.py
   ```

3. Verify data appears in both:
   - Check `social_data.json` file
   - View in web UI at http://localhost:5173/posts

### Test Monitoring Service

1. Start backend
2. Open frontend monitoring page
3. Start monitoring with 1-minute interval
4. Wait and observe:
   - Status updates every 5 seconds
   - Countdown timer decreases
   - After 1 minute, fetch occurs
   - Posts count increases

### Test Data Persistence

1. Add manual entry via CLI:
   ```bash
   python listener.py --add
   ```

2. Verify it appears in web UI:
   - Open http://localhost:5173/posts
   - Should see the new entry

3. Add manual entry via web UI

4. Run CLI and verify:
   ```bash
   python listener.py --dashboard
   open dashboard.html
   ```

## Performance Testing

### Backend Load Test

Use Apache Bench or similar:

```bash
# Install ab
brew install apache-bench  # macOS

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/api/health

# Test posts endpoint
ab -n 100 -c 5 http://localhost:8000/api/posts
```

### Frontend Load Test

Open multiple browser tabs and verify:
- No console errors
- API calls don't multiply unnecessarily
- React Query caching works

## Error Testing

### Test Error Handling

1. **Backend not running**
   - Start frontend only
   - Verify error messages appear
   - Check network errors are caught

2. **Invalid API requests**
   ```bash
   # Invalid monitoring interval
   curl -X POST http://localhost:8000/api/monitoring/start \
     -H "Content-Type: application/json" \
     -d '{"interval_minutes": 0}'

   # Should return 422 validation error
   ```

3. **Missing data files**
   ```bash
   # Rename data file
   mv social_data.json social_data.json.bak

   # Start backend - should create empty file
   # Verify no crashes

   # Restore
   mv social_data.json.bak social_data.json
   ```

## Browser Compatibility

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari

## Verification Checklist

### Backend
- [ ] All endpoints return correct status codes
- [ ] API documentation loads at /docs
- [ ] CORS headers present
- [ ] Validation errors return 422
- [ ] Server errors return 500
- [ ] Data persists to JSON files

### Frontend
- [ ] No console errors
- [ ] All pages load
- [ ] Charts render correctly
- [ ] Forms submit successfully
- [ ] Navigation works
- [ ] Responsive design works on mobile

### Docker
- [ ] Containers build successfully
- [ ] Backend accessible on port 8000
- [ ] Frontend accessible on port 3000
- [ ] API proxying works through nginx
- [ ] Containers restart on failure
- [ ] Volumes persist data

### CLI Compatibility
- [ ] `python listener.py` still works
- [ ] `python listener.py --watch` works
- [ ] `python listener.py --add` works
- [ ] Both CLI and web can read same data

## Troubleshooting Tests

If tests fail, check:

1. **Backend won't start**
   - Python version 3.12+
   - All requirements installed
   - Port 8000 not in use
   - .env file exists

2. **Frontend won't start**
   - Node.js 18+
   - npm dependencies installed
   - Port 5173 not in use

3. **API calls fail**
   - Backend running
   - CORS configured
   - Correct API URL in frontend/.env

4. **Docker fails**
   - Docker daemon running
   - Ports 3000, 8000 available
   - Sufficient disk space

## Automated Testing (Future)

To be implemented:

- Backend: pytest for API tests
- Frontend: Vitest + React Testing Library
- E2E: Playwright or Cypress
- CI/CD: GitHub Actions
