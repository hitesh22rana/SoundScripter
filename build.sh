# !/bin/bash

docker build -t transcription-service -f backend/Dockerfile.transcription-service .
cp frontend/.env.example frontend/.env
docker-compose -f docker-compose.yml up