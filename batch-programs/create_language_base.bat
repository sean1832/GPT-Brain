@echo off
cd..

echo Activating Virtural environment...
call .\venv\Scripts\activate

echo creating language base...
call python .\batch-programs\create_language_base.py

cls
echo language base created!

pause