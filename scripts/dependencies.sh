#!/bin/bash

# Navigate to the /backend directory
cd backend/

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
    echo "Virtualenv is not installed. Installing now..."
    if [[ "$OSTYPE" == "mswin" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" || "$OSTYPE" == "win64" || "$OSTYPE" == "msys" ]]; then
        # Install virtualenv using python on Windows
        python -m pip install virtualenv
    else
        # Install virtualenv using python3 on Unix-like systems
        python3 -m pip install virtualenv
    fi
fi

# Create a virtual environment if not present
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    virtualenv venv --python=python3.11
fi

# Activate the virtual environment
if [[ "$OSTYPE" == "mswin" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" || "$OSTYPE" == "win64" || "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install the required packages
pip3 install -r requirements.txt