#!/bin/bash

# Check if ffmpeg is installed on the system, exit if not
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found, please install it on your system, you can download it from https://ffmpeg.org/download.html, exiting..."
    exit
fi

# Navigate to the /backend directory
cd backend/

# Activate the virtual environment
if [[ "$OSTYPE" == "mswin" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" || "$OSTYPE" == "win64" || "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# check if .env file exists, if not, copy the .env.example file to .env
if [ ! -f ./.env ]; then
    cp ./.env.example ./.env
fi

export LOCAL_STORAGE_BASE_PATH=$(pwd)/data

# Run the task-queue
celery -A app.background_tasks worker --loglevel=info -P threads -E