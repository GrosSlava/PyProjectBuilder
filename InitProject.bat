@echo off


rem create enviroment
python -m venv venv

rem set enviroment
call %~dp0\venv\Scripts\activate.bat


rem .......................Requirements................................. rem

echo "------------------Tools-----------------"
python -m pip install --upgrade pip
pip install -r %~dp0\Requirements.txt
echo "----------------------------------------"

echo "------------Current veriosns------------"
python -V
pip -V
pip list
echo "----------------------------------------"

rem ................................................................... rem

pause
