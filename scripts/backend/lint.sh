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

# Lint the code
ruff check . --fix