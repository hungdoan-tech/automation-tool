@echo off
setlocal enabledelayedexpansion

:: Set main paths
set "SOURCE_PATH=%CD%"
set "SCRIPT_PATH=%SOURCE_PATH%\script"
set "VENV_PATH=%SOURCE_PATH%\venv"

:: Check if Python is installed
echo - Checking if Python is installed
call python --version >NUL 2>&1
if %errorlevel%==0 (
    echo - Python is already installed
) else (
    echo - Python is not installed, attempting to install
    call "%SCRIPT_PATH%\install_python.bat"
)

:: Check if virtual environment exists
echo - Checking if virtual environment exists
if not exist "%VENV_PATH%" (
    echo - Virtual environment is missing, attempting to install
    call "%SCRIPT_PATH%\create_virtual_env.bat"
)

:: Invoke the entry point with the virtual environment
echo - Invoking the entry point with the virtual environment
call "%VENV_PATH%\Scripts\activate"

set "ENTRY_POINT=%CD%"

:: Try to find and invoke the entry point to run console app
echo - Trying to find and invoke the console entry point at %ENTRY_POINT%
set "PYTHONPATH=%ENTRY_POINT%"
call python -m src.console.EntryPoint

call "%VENV_PATH%\Scripts\deactivate"

endlocal
pause
