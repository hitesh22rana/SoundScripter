#!/bin/bash

# Navigate to the /backend directory
cd backend/

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
    echo "Virtualenv is not installed. Installing now..."
    python3 -m pip install virtualenv
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