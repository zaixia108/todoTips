#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TodoTips 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TodoTips",
    version="1.0.0",
    author="TodoTips Contributors",
    description="快速待办事项管理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zaixia108/todoTips",
    py_modules=[
        'main',
        'todo_app',
        'todo_model',
        'main_window',
        'reminder_manager',
        'notification_manager',
        'settings_dialog'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires='>=3.6',
    install_requires=[
        'PySide6>=6.0.0',
        'keyboard>=0.13.5',
        'pyperclip>=1.8.2',
    ],
    extras_require={
        'sound': ['playsound>=1.3.0'],
        'win_notify': ['win10toast>=0.9'],
    },
    entry_points={
        'console_scripts': [
            'todotips=main:main',
        ],
    },
)
