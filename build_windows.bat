# Windows Batch Script to Build Executable
# Run this to create VulnerabilityScanner.exe

@echo off
echo Building Network Vulnerability Scanner...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Building executable...
python build/build_executable.py
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo Step 3: Build complete!
echo.
echo Executable location: dist\VulnerabilityScanner.exe
echo.
pause
