echo Checking library updates...
set "REQUIREMENTS=requirements.txt"
set "LAST_MODIFIED=requirements.temp"

rem Check if requirements.txt file exists
if not exist %REQUIREMENTS% (
  echo "Error: requirements.txt not found"
  exit /b 1
)

rem Check if last_modified.txt file exists
if not exist %LAST_MODIFIED% (
  echo 0>"%LAST_MODIFIED%"
)

rem Check if requirements.txt file has been modified
for %%a in (%REQUIREMENTS%) do set "mod_date=%%~ta"
set /p last_mod_date=<%LAST_MODIFIED%
if "%mod_date%" neq "%last_mod_date%" (
  pip3 install -r %REQUIREMENTS%
  echo %mod_date%>"%LAST_MODIFIED%"
  cls
  echo "Requirements file has been modified. Updated complete!"
) else (
  echo "Requirements file has not been modified. Skipping update."
)

rem copy example prompt to user folder without overwrite
xcopy "example_prompt\*.*" ".user\prompt" /I /E /Y /D
