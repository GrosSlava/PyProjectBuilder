@echo off



rem install needed tools
echo "------------------Tools-----------------"
python -m pip install --upgrade pip
echo "----------------------------------------"

rem create enviroment
python -m venv venv

rem set enviroment
call %~dp0\venv\Scripts\activate.bat

rem install requirements
pip install -r %~dp0\Requirements.txt

rem show versions
echo "------------Current veriosns------------"
python -V
pip -V
pip list
echo "----------------------------------------"

pause
