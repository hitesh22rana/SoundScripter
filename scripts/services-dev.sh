#!/bin/bash

# Run the redis container for pub-sub
docker run -d -p 6379:6379 --name pub-sub-dev redis:latest

# Run the postgres container for the database, with mount volumes
docker run -d -p 5432:5432 --name db-dev -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=db -v $PWD/backend/data:/var/lib/postgresql/data postgres:alpine

# Run the rabbitmq container for the message broker
docker run -d -p 5672:5672 --name message-broker-dev rabbitmq:latest

# Build transcription-service image
docker build -t transcription-service -f backend/Dockerfile.transcription-service .