@echo off
REM Network Vulnerability Scanner - Windows Launcher
REM Automatically installs dependencies and runs the application

echo.
echo ======================================
echo  Network Vulnerability Scanner
echo  Windows Launcher
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

REM Run the auto-installer
echo Starting auto-installer...
python install_and_run.py

if errorlevel 1 (
    echo.
    echo Failed to launch application
    pause
    exit /b 1
)

pause
