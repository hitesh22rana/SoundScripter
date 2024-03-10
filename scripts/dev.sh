#!/bin/bash

# Activate the virtual environment
if [[ "$OSTYPE" == "mswin" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" || "$OSTYPE" == "win64" || "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Run the FastAPI app
celery -A app.background_tasks worker --loglevel=info -P threads -E &
uvicorn app.main:app --reload