#!/bin/bash
# Verify that all required files are present for the web interface

echo "🔍 Social Media Listener - Installation Verification"
echo "===================================================="
echo ""

errors=0
warnings=0

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "❌ MISSING: $1"
        ((errors++))
    fi
}

# Function to check if directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $1/"
    else
        echo "❌ MISSING: $1/"
        ((errors++))
    fi
}

# Function to check optional file
check_optional() {
    if [ -f "$1" ]; then
        echo "✅ $1"
    else
        echo "⚠️  Optional: $1"
        ((warnings++))
    fi
}

echo "📦 Backend Files:"
check_dir "backend"
check_file "backend/main.py"
check_file "backend/config.py"
check_dir "backend/models"
check_dir "backend/routers"
check_dir "backend/services"
check_dir "backend/middleware"
echo ""

echo "🎨 Frontend Files:"
check_dir "frontend"
check_dir "frontend/src"
check_file "frontend/package.json"
check_file "frontend/vite.config.ts"
check_file "frontend/src/main.tsx"
check_file "frontend/src/App.tsx"
echo ""

echo "🐳 Docker Files:"
check_dir "docker"
check_file "docker/Dockerfile.backend"
check_file "docker/Dockerfile.frontend"
check_file "docker/nginx.conf"
check_file "docker-compose.yml"
echo ""

echo "⚙️  Configuration Files:"
check_file ".env.example"
check_file "frontend/.env.example"
check_optional ".env"
check_optional "frontend/.env"
echo ""

echo "📚 Documentation:"
check_file "README_WEB.md"
check_file "QUICKSTART.md"
check_file "TESTING.md"
check_file "IMPLEMENTATION_SUMMARY.md"
echo ""

echo "🔧 Scripts:"
check_file "start_backend.sh"
check_file "start_frontend.sh"
echo ""

echo "📝 Core Files:"
check_file "listener.py"
check_file "config.py"
check_file "requirements.txt"
echo ""

# Check Python version
echo "🐍 Python Version:"
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1)
    echo "✅ $python_version"

    # Check if version is 3.12+
    version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if (( $(echo "$version >= 3.12" | bc -l) )); then
        echo "✅ Python version is 3.12 or higher"
    else
        echo "⚠️  Python 3.12+ recommended (found $version)"
        ((warnings++))
    fi
else
    echo "❌ python3 not found"
    ((errors++))
fi
echo ""

# Check Node.js version
echo "📦 Node.js Version:"
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo "✅ $node_version"

    # Extract major version
    major=$(echo $node_version | cut -d. -f1 | sed 's/v//')
    if [ "$major" -ge 18 ]; then
        echo "✅ Node.js version is 18 or higher"
    else
        echo "⚠️  Node.js 18+ recommended (found v$major)"
        ((warnings++))
    fi
else
    echo "❌ node not found"
    ((errors++))
fi
echo ""

# Check npm
echo "📦 npm:"
if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    echo "✅ npm $npm_version"
else
    echo "❌ npm not found"
    ((errors++))
fi
echo ""

# Check Docker
echo "🐳 Docker:"
if command -v docker &> /dev/null; then
    docker_version=$(docker --version)
    echo "✅ $docker_version"
else
    echo "⚠️  Docker not found (optional for deployment)"
    ((warnings++))
fi
echo ""

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    compose_version=$(docker-compose --version)
    echo "✅ $compose_version"
else
    echo "⚠️  docker-compose not found (optional for deployment)"
    ((warnings++))
fi
echo ""

# Summary
echo "===================================================="
echo "📊 Summary:"
echo ""

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo "✅ Perfect! All required files and dependencies are present."
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Configure .env file: cp .env.example .env"
    echo "   2. Start backend: ./start_backend.sh"
    echo "   3. Start frontend: ./start_frontend.sh"
    echo "   4. Open http://localhost:5173"
    echo ""
    exit 0
elif [ $errors -eq 0 ]; then
    echo "⚠️  Installation complete with $warnings warning(s)."
    echo "   You can proceed, but some optional features may not work."
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Configure .env file: cp .env.example .env"
    echo "   2. Start backend: ./start_backend.sh"
    echo "   3. Start frontend: ./start_frontend.sh"
    echo "   4. Open http://localhost:5173"
    echo ""
    exit 0
else
    echo "❌ Installation incomplete with $errors error(s) and $warnings warning(s)."
    echo "   Please fix the errors above before proceeding."
    echo ""
    echo "💡 Common fixes:"
    echo "   - Install Python 3.12+: https://www.python.org/downloads/"
    echo "   - Install Node.js 18+: https://nodejs.org/"
    echo "   - Install Docker: https://docs.docker.com/get-docker/"
    echo ""
    exit 1
fi
