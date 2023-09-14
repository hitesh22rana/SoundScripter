# !/bin/bash

celery -A app.background_tasks.transcription worker --loglevel=info -P gevent -E &
uvicorn app.main:app --host 0.0.0.0 --port 8000