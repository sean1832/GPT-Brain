@echo off

echo Activating Virtural environment...
call .\venv\Scripts\activate

call .\update.bat

streamlit run Seanium_Brain.py