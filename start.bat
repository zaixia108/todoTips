@echo off
REM TodoTips 启动脚本 (Windows)

echo 正在启动 TodoTips...

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python
    pause
    exit /b 1
)

REM 检查依赖
echo 检查依赖...
python -c "import PySide2" >nul 2>&1
if errorlevel 1 (
    echo 未安装依赖，正在安装...
    pip install -r requirements.txt
)

REM 启动应用
echo 启动应用...
python main.py
