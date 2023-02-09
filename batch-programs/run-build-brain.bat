@echo off
cd..
echo Activating Virtural environment...
call .\venv\Scripts\activate

echo building brain...
python build-brain.py
echo complete building brain!