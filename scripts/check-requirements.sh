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

# Checks if port 5672, 6379, 8000 and 3000 are free and open
for port in 5672 6379 8000 3000; do
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

echo "Success: All requirements are met"
exit 0