#!/bin/bash

# Checks if a minimum of 4 CPU threads are available
min_cpu_threads=4
available_cpu_threads=$(getconf _NPROCESSORS_CONF)

if [ "$available_cpu_threads" -lt "$min_cpu_threads" ]; then
    echo "Error: Insufficient CPU threads. This application requires a minimum of $min_cpu_threads CPU threads, but your system has only $available_cpu_threads CPU threads."
    exit 1
fi

# Checks if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Checks if Docker is running
if ! docker info &> /dev/null; then
    echo "Error: Docker is installed but not running. Please start Docker and try again."
    exit 1
fi

# Checks if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Checks if port 5432, 5672, 6379 are free and open
for port in 5432, 5672, 6379; do
    if [[ "$OSTYPE" == "msys" ]]; then
        if netstat -an | findstr ":$port"; then
            echo "Error: Port $port is already in use. Please free up port $port and try again."
            exit 1
        fi
        
    else
        if nc -zv localhost $port 2>/dev/null; then
            echo "Error: Port $port is already in use. Please free up port $port and try again."
            exit 1
        fi
    fi
done

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
    docker run -d -p 5432:5432 --name db-dev -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=db -v $PWD/backend/data/db:/var/lib/postgresql/data postgres:alpine
fi

# Run the rabbitmq container for the message broker
docker run -d -p 5672:5672 --name message-broker-dev rabbitmq:latest

# Build transcription-service image
docker build -t transcription-service -f backend/Dockerfile.transcription-service .