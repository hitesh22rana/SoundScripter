#!/bin/bash

# Navigate to the /backend directory
cd backend/

# Activate the virtual environment
if [[ "$OSTYPE" == "mswin" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" || "$OSTYPE" == "win64" || "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Check if isort is already installed
if ! command -v isort &> /dev/null; then
    echo "isort is not installed. Installing now..."
    pip3 install isort
fi

# Check if ruff is already installed
if ! command -v ruff &> /dev/null; then
    echo "ruff is not installed. Installing now..."
    pip3 install ruff
fi


# Run isort and ruff to format the Python code
isort . && ruff format .