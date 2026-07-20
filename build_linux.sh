#!/bin/bash
# Linux/macOS build script

echo "Building Network Vulnerability Scanner..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10+ and try again"
    exit 1
fi

echo "Step 1: Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "Step 2: Building executable..."
python3 build/build_executable.py
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo ""
echo "Step 3: Build complete!"
echo ""
echo "Executable location: dist/VulnerabilityScanner"
echo ""
