#!/bin/bash

celery -A app.background_tasks worker --loglevel=info -P threads -E &
uvicorn app.main:app --host 0.0.0.0 --port 8000