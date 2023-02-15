@echo off
cd..
echo Activating Virtual environment...
call .\venv\Scripts\activate

echo updating pip...
python -m pip install --upgrade pip

echo updating requirements...
pip3 install -r requirements.txt
ping 127.0.0.1 -n 2 > NUL
echo requirements updated complete!
pause