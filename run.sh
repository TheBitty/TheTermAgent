#!/bin/bash
# TermSage startup script

# Check if we have the required dependencies
if ! python -c "import requests" 2>/dev/null; then
    echo "Missing dependencies. Installing requests..."
    pip install --user requests
fi

# Run TermSage
echo "Starting TermSage..."
cd "$(dirname "$0")/src"
python main.py