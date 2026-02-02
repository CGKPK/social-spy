#!/bin/bash
# Start the React frontend development server

echo "Starting Social Media Listener Frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# Start development server
echo "Starting frontend on http://localhost:5173"
npm run dev
