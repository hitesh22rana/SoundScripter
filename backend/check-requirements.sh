#!/bin/bash

# Checks if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Checks if Docker is running
if ! docker info &> /dev/null; then
    echo "Docker is installed but not running. Please start Docker and try again."
    exit 1
fi

# Checks if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

echo "Docker is installed and running."
exit 0