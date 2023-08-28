#!/bin/bash

# Activate the virtual environment
source venv/Scripts/activate

# Run isort and black to format the Python code
isort . && black .