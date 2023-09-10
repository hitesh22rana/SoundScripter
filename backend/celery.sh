#!/bin/bash

# Activate the virtual environment
source venv/Scripts/activate

# Run the FastAPI app
celery -A app.background_tasks.transcription worker --loglevel=info -P gevent