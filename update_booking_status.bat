@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python manage.py update_booking_status
deactivate 