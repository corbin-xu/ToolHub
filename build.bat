@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo [build] 正在用 PyInstaller 打包 exe...
python -m PyInstaller --noconfirm --clean ToolHub.spec
if errorlevel 1 (
    echo [build] PyInstaller 失败
    exit /b 1
)

if not exist "dist\ToolHub.exe" (
    echo [build] 未找到 dist\ToolHub.exe
    exit /b 1
)
echo [build] 已生成 dist\ToolHub.exe

echo [build] 正在用 Inno Setup 打包安装程序...
set "ISCC="
where iscc >nul 2>&1 && set "ISCC=iscc"
if "%ISCC%"=="" if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if "%ISCC%"=="" if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if "%ISCC%"=="" (
    echo [build] 未找到 Inno Setup，跳过安装包。请安装 Inno Setup 6 后重试。
    echo [build] 仅完成 exe 打包: dist\ToolHub.exe
    exit /b 0
)

"%ISCC%" setup.iss
if errorlevel 1 (
    echo [build] Inno Setup 失败
    exit /b 1
)

echo [build] 完成。安装包: dist\ToolHub-1.4.exe
exit /b 0
