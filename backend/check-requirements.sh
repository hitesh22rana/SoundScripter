# !/bin/bash

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

# Checks if port 8000, 5672, 6379 and 5432 are free and open
for port in 8000 5672 6379 5432; do
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