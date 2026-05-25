@echo off
setlocal

set "INDEX_FILE=%~dp0index.html"
set "CHROME_PATH=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
set "CHROME_PATH_X86=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
set "CHROME_PATH_LOCAL=%LocalAppData%\Google\Chrome\Application\chrome.exe"

if exist "%CHROME_PATH%" (
    start "" "%CHROME_PATH%" "%INDEX_FILE%"
    exit /b 0
)

if exist "%CHROME_PATH_X86%" (
    start "" "%CHROME_PATH_X86%" "%INDEX_FILE%"
    exit /b 0
)

if exist "%CHROME_PATH_LOCAL%" (
    start "" "%CHROME_PATH_LOCAL%" "%INDEX_FILE%"
    exit /b 0
)

start "" "%INDEX_FILE%"
