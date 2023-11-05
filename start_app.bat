@echo off

setlocal enabledelayedexpansion

:find_onedrive_mapping_folder
set "searchTerm=OneDrive "
set "OneDriveFolder=Documents"
for /d %%D in ("%USERPROFILE%\*") do (
    for %%F in ("%%~nxD") do (
        set "folderName=%%~nF"
        if /I "!folderName:~0,9!"=="!searchTerm!" (
            set "OneDriveFolder=%%~nF"
            goto :set_main_paths
        )
    )
)

:set_main_paths
set SOURCE_PATH=%USERPROFILE%\%OneDriveFolder%\automation_tool
set SCRIPT_PATH=%SOURCE_PATH%\script
set VENV_PATH=%SOURCE_PATH%\venv

echo - Checking Python is exist or not
call python --version 2>NUL
if %errorlevel%==0 (
    goto :check_virtual_env
) else (
    echo - Python is not installed in the machine, we will try to install
    call "%SCRIPT_PATH%"\install_python.bat
)

:check_virtual_env
echo - Check virtual environment is exist or not
if not exist "%VENV_PATH%" (
    echo Virtual Environment is missing, we will try to install
    call "%SCRIPT_PATH%"\create_virtual_env.bat
)

:check_source
echo - Checking source code is exist or not
if not exist "%SOURCE_PATH%" (
    echo Source code is missing, we will try to install
    call "%SCRIPT_PATH%"\download_source_code.bat
)

:check_input_file
echo - Checking the mandatory input file is exist or not
if not exist "%SOURCE_PATH%"\input\settings.input (
    echo Please provide the settings.input with mandatory info at "%SOURCE_PATH%"\input\settings.input
    goto :eof
)

:invoke_file
echo - Invoking the entry point with virtual environment
call "%VENV_PATH%"\Scripts\activate

call python "%SOURCE_PATH%"\src\Entry_Point.py

call "%VENV_PATH%"\Scripts\deactivate

endlocal
:eof