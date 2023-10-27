#!/bin/bash

# Activate the virtual environment
source venv/Scripts/activate

# Run the FastAPI app
celery -A app.background_tasks worker --loglevel=info -P threads -E &
uvicorn app.main:app --reload