#!/bin/bash

# Run the redis container for pub-sub
docker run -d -p 6379:6379 --name pub-sub-dev redis:latest

# Run the postgres container for the database
if [[ "$OSTYPE" == "mswin" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" || "$OSTYPE" == "win64" || "$OSTYPE" == "msys" ]]; then
    # Host path
    WORKING_DIR="$(pwd | sed 's/\//\\\\/g')"
    HOST_PATH="$WORKING_DIR\\\backend\\\data\\\db"
    
    HOST_PATH=${HOST_PATH#*\\\\}
    HOST_PATH="${HOST_PATH^}"
    HOST_PATH="${HOST_PATH::1}:\\${HOST_PATH:2}"
    
    docker run -d -p 5432:5432 --name db-dev -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=db -v $HOST_PATH:/var/lib/postgresql/data postgres:alpine
else
    docker run -d -p 5432:5432 --name db-dev -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=db -v $PWD/backend/data:/var/lib/postgresql/data postgres:alpine
fi

# Run the rabbitmq container for the message broker
docker run -d -p 5672:5672 --name message-broker-dev rabbitmq:latest

# Build transcription-service image
docker build -t transcription-service -f backend/Dockerfile.transcription-service .