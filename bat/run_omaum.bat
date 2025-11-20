@echo off
setlocal

set "PROJECT_ROOT=%~dp0.."
pushd "%PROJECT_ROOT%"

if exist ".venv\Scripts\python.exe" (
	set "PYTHON_CMD=.venv\Scripts\python.exe"
) else (
	set "PYTHON_CMD=python"
)

"%PYTHON_CMD%" bat\run_omaum.py

popd
endlocal