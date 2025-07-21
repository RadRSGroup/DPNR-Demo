#!/bin/bash
# Render startup script for ModAgents

set -e  # Exit on error

echo "🚀 Starting ModAgents on Render..."

# Set default port if not provided
export PORT=${PORT:-8000}

# Ensure Python path is set
export PYTHONPATH=${PYTHONPATH:-/app/src}

# Start the application with uvicorn
echo "Starting API server on port $PORT"
exec uvicorn src.frontend_api_server:app --host 0.0.0.0 --port $PORT --workers 1