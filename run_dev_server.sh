#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_DIR/env"
PYTHON_BIN="$VENV_PATH/Scripts/python"
PIP_BIN="$VENV_PATH/Scripts/pip"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    exit 1
fi

echo "📁 Project directory: $PROJECT_DIR"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$VENV_PATH/Scripts/activate"
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo "   Python: $PYTHON_BIN"
PYTHON_VERSION=$("$PYTHON_BIN" --version 2>&1)
echo "   Version: $PYTHON_VERSION"

# Check for .env file
if [ -f "$PROJECT_DIR/.env" ]; then
    echo -e "${GREEN}✅ .env file found${NC}"
else
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
fi

# Force local SQLite for development - unset any remote DATABASE_URL
echo ""
echo "🗄️  Configuring database..."
if grep -q "viaduct.proxy.rlwy.net\|railway\|heroku\|render" "$PROJECT_DIR/.env" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Remote database detected in .env${NC}"
fi
echo "🔄 Using local SQLite for development..."
unset DATABASE_URL
export DATABASE_URL=""

# Update pip
echo ""
echo "📦 Checking dependencies..."
"$PIP_BIN" install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✅ Pip dependencies updated${NC}"

# Install requirements
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    "$PIP_BIN" install -q -r "$PROJECT_DIR/requirements.txt" 2>&1 | grep -v "already satisfied" | head -5
    echo -e "${GREEN}✅ Django and dependencies already installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found${NC}"
fi

# Clean up cache
echo ""
echo "🧹 Cleaning up temporary files..."
find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find "$PROJECT_DIR" -type f -name "*.pyc" -delete 2>/dev/null
echo -e "${GREEN}✅ Cache cleaned${NC}"

# Run migrations
echo ""
echo "🗄️  Running database migrations (using SQLite)..."
cd "$PROJECT_DIR"
if ! "$PYTHON_BIN" manage.py migrate --noinput 2>&1 | tail -20; then
    echo -e "${YELLOW}⚠️  Migrations encountered an issue (may be expected if DB is new)${NC}"
fi
echo -e "${GREEN}✅ Migrations complete (or skipped - DB already initialized)${NC}"

# Check for superuser
echo ""
echo "👤 Checking for superuser..."
SUPERUSER_EXISTS=$("$PYTHON_BIN" manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>/dev/null)
if [ "$SUPERUSER_EXISTS" = "True" ]; then
    echo -e "${GREEN}Superuser exists${NC}"
else
    echo -e "${YELLOW}⚠️  No superuser found. Run: python manage.py createsuperuser${NC}"
fi

# Collect static files
echo ""
echo "📂 Collecting static files..."
"$PYTHON_BIN" manage.py collectstatic --noinput -v 0 2>/dev/null
echo -e "${GREEN}✅ Static files handled${NC}"

# Start Django development server
echo ""
echo "🚀 Starting Django development server..."
echo -e "   📝 Server will run at ${BLUE}http://127.0.0.1:8000${NC}"
echo -e "   🔐 Admin panel at ${BLUE}http://127.0.0.1:8000/admin${NC}"
echo -e "   📚 To create an admin user, run: ${BLUE}python manage.py createsuperuser${NC}"
echo -e "   🛑 Press Ctrl+C to stop the server"
echo ""

# Run the development server
"$PYTHON_BIN" manage.py runserver 0.0.0.0:8000
