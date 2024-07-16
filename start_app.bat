@echo off
setlocal enabledelayedexpansion

:: Set main paths
set "SOURCE_PATH=%CD%"
set "SCRIPT_PATH=%SOURCE_PATH%\script"
set "VENV_PATH=%SOURCE_PATH%\venv"

:: Check if Python is installed and is version 3.10
echo - Checking if Python 3.10 is installed
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i

if not defined PYTHON_VERSION (
    echo - Python is not installed, attempting to install
    call "%SCRIPT_PATH%\install_python.bat"
)

for /f "tokens=1,2 delims=." %%i in ("%PYTHON_VERSION%") do (
    set MAJOR_VERSION=%%i
    set MINOR_VERSION=%%j
)

if "%MAJOR_VERSION%" NEQ "3" (
    echo - Python is installed, but not 3.10 version, attempting to install
    call "%SCRIPT_PATH%\install_python.bat"
)

if "%MINOR_VERSION%" NEQ "10" (
    echo - Python is installed, but not 3.10 version, attempting to install
    call "%SCRIPT_PATH%\install_python.bat"
)

echo - Python 3.10 is already installed

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

:: Determine which entry point to invoke based on the argument
set "PYTHONPATH=%ENTRY_POINT%"
if "%~1"== "console" (
    echo - Trying to find and invoke the console entry point at %ENTRY_POINT%
    call python -m src.console.EntryPoint
) else if "%~1"=="" or "gui" (
    echo - Trying to find and invoke the GUI entry point at %ENTRY_POINT%
    call python -m src.gui.GUIApp
) else (
    echo Invalid argument. Usage: %0 [console|gui]
)

call "%VENV_PATH%\Scripts\deactivate"

endlocal
pause
