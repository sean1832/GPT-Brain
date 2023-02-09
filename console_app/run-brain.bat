@echo off
cd..
echo Activating Virtural environment...
call .\venv\Scripts\activate

rem checking if input.txt is updated
python console_app\check_update.py

setlocal enabledelayedexpansion
set "tempFile=.user\input_sig.temp"

for /f "usebackq delims=" %%a in ("%tempFile%") do (
    set "tempValue=%%a"
)

if "%tempValue%" == "not updated" (
    goto end
) else (
    call batch-programs\run-build-brain.bat
    cls
    echo Brain updated!
)


:end
echo running brain...
python console_app\brain.py