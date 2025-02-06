#!/bin/bash
# Exit on error and print each command
set -ex

echo "Python version:"
python --version

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p instance
mkdir -p app/static/uploads

echo "Running database migrations..."
python -m flask db upgrade || {
    echo "Error running migrations"
    exit 1
}

echo "Creating database tables..."
python -c "from run import app; from app import db; app.app_context().push(); db.create_all()"

echo "Build completed successfully!"
