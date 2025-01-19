<<<<<<< HEAD
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python manage.py update_booking_status
=======
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python manage.py update_booking_status
>>>>>>> 29e35e4892c15854585299d3eee6ff215d96cbb2
deactivate 