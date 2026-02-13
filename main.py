#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TodoTips - 快速待办事项管理工具
"""

import sys
import os
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from todo_app import TodoApplication

def main():
    # 设置高DPI缩放
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 设置应用程序信息
    app.setApplicationName("TodoTips")
    app.setOrganizationName("TodoTips")
    
    todo_app = TodoApplication()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
