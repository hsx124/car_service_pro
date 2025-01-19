@echo off
setlocal enabledelayedexpansion

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Set the path to the virtual environment Python
set PYTHON_PATH=venv\Scripts\python.exe

REM Check if Python exists
if not exist %PYTHON_PATH% (
    echo Error: Python not found at %PYTHON_PATH%
    echo Please make sure the virtual environment is set up correctly.
    exit /b 1
)

REM Run the Django command
%PYTHON_PATH% manage.py update_booking_status > logs\booking_status.log 2>&1

REM Check the error level
if !errorlevel! neq 0 (
    echo Error: Command failed. Check logs\booking_status.log for details.
    exit /b !errorlevel!
)

echo Command completed successfully.
exit /b 0 