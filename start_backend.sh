#!/bin/bash
# Start the FastAPI backend server

echo "Starting Social Media Listener Backend..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your API keys, then restart."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start the server
echo "Starting server on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
