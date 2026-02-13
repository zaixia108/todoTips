#!/bin/bash
# TodoTips 启动脚本

echo "正在启动 TodoTips..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
python3 -c "import PySide6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "未安装依赖，正在安装..."
    pip3 install -r requirements.txt
fi

# 启动应用
echo "启动应用..."
python3 main.py
