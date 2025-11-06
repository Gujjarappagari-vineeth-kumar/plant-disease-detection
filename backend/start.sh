#!/bin/bash
# Startup script for Render deployment
export PORT=${PORT:-8000}
echo "Starting server on port $PORT"
echo "Python path: $PYTHONPATH"
echo "Current directory: $(pwd)"
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
