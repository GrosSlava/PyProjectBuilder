rem Copyright (c) 2022-2023 GrosSlava
@echo off



:begin
rem Install needed tools
echo "------------------Tools-----------------"
python -m pip install --upgrade pip
echo "----------------------------------------"

rem Create enviroment
python -m venv venv

rem Set enviroment
call "%~dp0\venv\Scripts\activate.bat"

rem Install requirements
pip install -r "%~dp0\Requirements.txt"

rem Show versions
echo "------------Current veriosns------------"
python -V
pip -V
pip list
echo "----------------------------------------"

:end
pause
