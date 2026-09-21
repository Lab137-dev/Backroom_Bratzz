@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating Backroom Bratzz environment...
  py -3 -m venv .venv || goto :error
  ".venv\Scripts\python.exe" -m pip install --upgrade pip || goto :error
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto :error
)
".venv\Scripts\python.exe" run_game.py
if errorlevel 1 goto :error
exit /b 0
:error
echo.
echo Backroom Bratzz could not start. See the message above.
pause
exit /b 1

