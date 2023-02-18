@echo off
cd..

echo Activating Virtural environment...
call .\venv\Scripts\activate

echo creating language base...
call python .\batch-programs\create_language_base.py

echo updating .po files...
call python .\batch-programs\update_language.py
pause