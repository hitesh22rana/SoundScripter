# !/bin/bash

docker build -t transcription-service -f backend/Dockerfile.transcription-service .
docker-compose -f docker-compose.yml up