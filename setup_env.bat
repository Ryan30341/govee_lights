@echo off
REM Setup Python virtual environment for Govee Lights project

echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Environment setup complete!
echo To activate the environment, run: venv\Scripts\activate.bat

