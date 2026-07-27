@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=python"
where python >nul 2>&1
if not errorlevel 1 goto python_found
if exist "%LocalAppData%\Programs\Python\Python312\python.exe" set "PYTHON=%LocalAppData%\Programs\Python\Python312\python.exe"
if exist "%LocalAppData%\Programs\Python\Python312\python.exe" goto python_found
echo [build] ERROR: Python was not found.
exit /b 1

:python_found
echo [build] Building jd-supplier-label-generator.exe with PyInstaller...
"%PYTHON%" -m PyInstaller --noconfirm --clean jd-supplier-label-generator.spec
if errorlevel 1 goto pyinstaller_failed
if not exist "dist\jd-supplier-label-generator.exe" goto pyinstaller_missing
echo [build] Created dist\jd-supplier-label-generator.exe

set "ISCC="
where iscc >nul 2>&1
if not errorlevel 1 set "ISCC=iscc"
if defined ISCC goto inno_found
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if defined ISCC goto inno_found
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if defined ISCC goto inno_found
if exist "D:\Inno Setup 6\ISCC.exe" set "ISCC=D:\Inno Setup 6\ISCC.exe"
if defined ISCC goto inno_found
goto inno_missing

:inno_found
echo [build] Building the installer with Inno Setup...
"%ISCC%" "setup.iss"
if errorlevel 1 goto inno_failed
echo [build] Created dist\jd-supplier-label-generator-1.6.exe
exit /b 0

:pyinstaller_failed
echo [build] ERROR: PyInstaller failed.
exit /b 1

:pyinstaller_missing
echo [build] ERROR: dist\jd-supplier-label-generator.exe was not created.
exit /b 1

:inno_missing
echo [build] ERROR: Inno Setup 6 was not found.
exit /b 1

:inno_failed
echo [build] ERROR: Inno Setup failed.
exit /b 1
