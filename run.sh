#!/bin/bash

# Network Vulnerability Scanner - Linux/macOS Launcher
# Automatically installs dependencies and runs the application

echo ""
echo "======================================"
echo " Network Vulnerability Scanner"
echo " Linux/macOS Launcher"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.10+ is required"
    echo "Current version: $python_version"
    exit 1
fi

# Run the auto-installer
echo "Starting auto-installer..."
python3 install_and_run.py

exit $?
