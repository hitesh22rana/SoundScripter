#!/bin/bash

# Activate the virtual environment
source venv/Scripts/activate

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