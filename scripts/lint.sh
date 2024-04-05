#!/bin/bash

# Navigate to the /backend directory
cd backend/

# Activate the virtual environment
if [[ "$OSTYPE" == "mswin" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" || "$OSTYPE" == "win64" || "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Check if ruff is already installed
if ! pip3 show ruff &>/dev/null; then
    echo "ruff is not installed. Installing now..."
    pip3 install ruff
fi

# Check if the --fix argument is provided
if [[ "$1" == "--fix" ]]; then
    ruff check . --fix
else
    ruff check .
fi