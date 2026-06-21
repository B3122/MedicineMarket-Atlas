@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

:: ============================================================
::  Market Research System - Windows 安装脚本
:: ============================================================

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║      医药健康产品市场研究系统 - Windows 安装程序          ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

:: -----------------------------------------------------------
::  步骤 0: 前置条件检查
:: -----------------------------------------------------------
echo [0/6] 正在检查前置条件...

:: 检查当前目录是否为仓库根目录
if not exist "requirements.txt" (
    echo [错误] 未在仓库根目录中找到 requirements.txt
echo          请确保在仓库根目录下运行此脚本。
    pause
    exit /b 1
)

echo          ✓ 当前目录看起来是仓库根目录

:: -----------------------------------------------------------
::  步骤 1: 检测 Python 3
:: -----------------------------------------------------------
echo.
echo [1/6] 正在检测 Python 3...

python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python。请安装 Python 3.8 或更高版本：
    echo          https://www.python.org/downloads/
    echo          安装时请务必勾选 "Add Python to PATH"
    pause
    exit /b 1
)

for /f "tokens=*" %%a in ('python --version 2^>^&1') do set PYTHON_VERSION=%%a
echo          ✓ 检测到 %PYTHON_VERSION%

:: -----------------------------------------------------------
::  步骤 2: 检测 Node.js / npm
:: -----------------------------------------------------------
echo.
echo [2/6] 正在检测 Node.js 和 npm...

npm --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 npm。请安装 Node.js（包含 npm）：
    echo          https://nodejs.org/en/download/
    pause
    exit /b 1
)

for /f "tokens=*" %%a in ('npm --version 2^>^&1') do set NPM_VERSION=%%a
echo          ✓ 检测到 npm v%NPM_VERSION%

:: -----------------------------------------------------------
::  步骤 3: 检测 Pi CLI
:: -----------------------------------------------------------
echo.
echo [3/6] 正在检测 Pi CLI...

pi --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 Pi CLI（pi 命令不可用）
    echo          某些功能可能需要 Pi CLI。如果已安装 OhMyOpenCode，
    echo          请确保 pi 命令已添加到系统 PATH 中。
    echo          继续安装其他依赖...
) else (
    for /f "tokens=*" %%a in ('pi --version 2^>^&1') do set PI_VERSION=%%a
    echo          ✓ 检测到 Pi CLI: %PI_VERSION%
)

:: -----------------------------------------------------------
::  步骤 4: 安装 Python 依赖
:: -----------------------------------------------------------
echo.
echo [4/6] 正在安装 Python 依赖...

pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] Python 依赖安装失败。请检查网络连接或 requirements.txt 内容。
    pause
    exit /b 1
)

echo          ✓ Python 依赖安装完成

:: -----------------------------------------------------------
::  步骤 5: 注册 Pi/OpenCode 插件（用户级，避免项目级冲突）
:: -----------------------------------------------------------
echo.
echo [5/6] 正在注册 Pi/OpenCode 插件...

pi --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 Pi CLI，跳过插件注册。
    echo          请在安装 Pi CLI 后手动运行以下命令（用户级）：
    echo            pi install npm:pi-web-access
    echo            pi install npm:pi-subagents
    echo          请勿使用 pi install -l，以免与 ~/.config/opencode 下
    echo          的用户级配置发生冲突。
    goto :SKIP_PLUGINS
)

echo          正在以用户级方式注册插件（不会写入项目级配置）...

call :INSTALL_PI_PLUGIN pi-web-access
if errorlevel 1 (
    echo [警告] pi-web-access 注册失败，请稍后手动运行：pi install npm:pi-web-access
)

call :INSTALL_PI_PLUGIN pi-subagents
if errorlevel 1 (
    echo [警告] pi-subagents 注册失败，请稍后手动运行：pi install npm:pi-subagents
)

goto :SKIP_PLUGINS

:INSTALL_PI_PLUGIN
pi list 2>nul | findstr /C:"  npm:%~1" >nul
if not errorlevel 1 (
    echo          ✓ %~1 已注册
    exit /b 0
)
echo          正在安装 %~1 ...
pi install npm:%~1
if errorlevel 1 (
    echo [警告] %~1 安装失败
    exit /b 1
)
echo          ✓ %~1 安装完成
exit /b 0

:SKIP_PLUGINS

:: -----------------------------------------------------------
::  步骤 6: 检测 Bash 环境（Git Bash / WSL）
:: -----------------------------------------------------------
echo.
echo [6/6] 正在检测 Bash 环境...

set BASH_FOUND=0

:: 检测 Git Bash
git --version >nul 2>&1
if not errorlevel 1 (
    bash --version >nul 2>&1
    if not errorlevel 1 (
        echo          ✓ 检测到 Git Bash 环境
        set BASH_FOUND=1
    )
)

:: 检测 WSL
wsl --version >nul 2>&1
if not errorlevel 1 (
    echo          ✓ 检测到 WSL (Windows Subsystem for Linux)
    set BASH_FOUND=1
)

if "%BASH_FOUND%"=="0" (
    echo [警告] 未检测到 Git Bash 或 WSL。
    echo          注意：competitor-analyst 代理需要 bash 工具支持。
    echo          建议安装以下之一：
    echo            - Git for Windows（包含 Git Bash）:
    echo              https://git-scm.com/download/win
    echo            - WSL (Windows Subsystem for Linux):
    echo              以管理员身份运行 PowerShell，执行：
    echo              wsl --install
    echo.
    echo          安装完成后，请重新运行此脚本或手动验证。
)

:: -----------------------------------------------------------
::  安装完成总结
:: -----------------------------------------------------------
echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║                   安装完成！                              ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.
echo  已完成的操作：
echo    • Python 依赖已安装（jsonschema, openpyxl 等）
if exist ".pi\npm\node_modules" (
echo    • npm 依赖已安装
)
if "%BASH_FOUND%"=="1" (
echo    • Bash 环境已确认可用
) else (
echo    • Bash 环境未检测到（见上方警告）
)
echo.
echo  ⚠  重要提示：Exa AI API 密钥
echo     pi-web-access 使用 Exa AI 进行网络搜索。
echo     插件内置的 Exa 额度有限，用完后将无法继续获取网页信息。
echo     请自行前往 https://exa.ai 注册并获取 API 密钥，
echo     然后在 Pi 的配置中设置（参考 ~/.pi/web-search.json）：
echo       { "provider": "exa", "exaApiKey": "YOUR_API_KEY" }
echo.
echo  下一步：
echo    1. 创建研究项目：在 projects/ 目录下新建文件夹，
echo       并添加 brief.md 和 config.json
echo    2. 运行研究流程：
echo       pi
echo       /run-chain full-market-review -- projects\brief.md
echo.

pause
endlocal
exit /b 0
