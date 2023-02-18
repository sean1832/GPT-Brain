@echo off
echo Creating Virtural environment folder...

python -m venv venv
echo Virtural environment created successfully!
ping 127.0.0.1 -n 2 > NUL


echo Activating Virtural environment!
call .\venv\Scripts\activate

echo updating pip
python -m pip install --upgrade pip


pip3 install -r requirements.txt
ping 127.0.0.1 -n 2 > NUL
echo Virtual requirements installed successfully!
cls

echo Creating OpenAI API keys profile...
REM if .user\ not exist, create one
if not exist .user\ (md .user\)

REM Create API KEY file
if not exist .user\API-KEYS.txt (
    set /p API_KEYS=[Enter your API keys]:
    echo %API_KEYS%> .user\API-KEYS.txt
    echo API key written to file!
)


REM copy example prompt
if not exist .user\prompt (md .user\prompt)
xcopy "example_prompt\*.*" ".user\prompt" /s /i

REM wait 2 tick
ping 127.0.0.1 -n 2 > NUL

REM create input txt file
if not exist .user\input.txt (
    echo.> .user\input.txt
    echo input file created!
)


python web_ui/initial_file_creator.py

echo Setup complete! Exiting...



pause