#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TodoApplication - 主应用程序类
"""

import os
import sys
import json
from datetime import datetime, timedelta
from PySide2.QtWidgets import (QSystemTrayIcon, QMenu, QAction, QMessageBox)
from PySide2.QtCore import QTimer, QThread, Signal, QSettings
from PySide2.QtGui import QIcon
import pyperclip
import keyboard

from main_window import MainWindow
from reminder_manager import ReminderManager
from notification_manager import NotificationManager
from todo_model import TodoModel


class HotkeyWorker(QThread):
    """全局快捷键监听线程"""
    quick_add_triggered = Signal()
    show_window_triggered = Signal()
    
    def __init__(self, quick_add_key='ctrl+shift+a', show_window_key='ctrl+shift+t'):
        super().__init__()
        self.quick_add_key = quick_add_key
        self.show_window_key = show_window_key
        self.running = True
    
    def run(self):
        """运行快捷键监听"""
        try:
            keyboard.add_hotkey(self.quick_add_key, self.on_quick_add)
            keyboard.add_hotkey(self.show_window_key, self.on_show_window)
            
            while self.running:
                keyboard.wait()
        except Exception as e:
            print(f"快捷键监听错误: {e}")
    
    def on_quick_add(self):
        """快速添加触发"""
        self.quick_add_triggered.emit()
    
    def on_show_window(self):
        """显示窗口触发"""
        self.show_window_triggered.emit()
    
    def stop(self):
        """停止监听"""
        self.running = False
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass


class TodoApplication:
    """待办事项应用程序主类"""
    
    def __init__(self):
        self.settings = QSettings()
        self.model = TodoModel()
        self.reminder_manager = ReminderManager()
        self.notification_manager = NotificationManager()
        
        # 创建主窗口
        self.main_window = MainWindow(self.model)
        
        # 创建系统托盘
        self.create_tray_icon()
        
        # 将托盘图标传递给通知管理器以实现跨平台通知
        self.notification_manager.tray_icon = self.tray_icon
        
        # 设置提醒回调
        self.reminder_manager.reminder_triggered.connect(self.on_reminder)
        
        # 启动快捷键监听
        self.setup_hotkeys()
        
        # 加载数据
        self.model.load_data()
        
        # 更新提醒
        self.update_reminders()
    
    def create_tray_icon(self):
        """创建系统托盘图标"""
        self.tray_icon = QSystemTrayIcon()
        
        # 使用默认图标（可以后续替换）
        icon = self.main_window.style().standardIcon(
            self.main_window.style().SP_MessageBoxInformation
        )
        self.tray_icon.setIcon(icon)
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        show_action = QAction("显示主窗口", tray_menu)
        show_action.triggered.connect(self.show_main_window)
        tray_menu.addAction(show_action)
        
        quick_add_action = QAction("快速添加", tray_menu)
        quick_add_action.triggered.connect(self.quick_add_from_clipboard)
        tray_menu.addAction(quick_add_action)
        
        tray_menu.addSeparator()
        
        settings_action = QAction("设置", tray_menu)
        settings_action.triggered.connect(self.show_settings)
        tray_menu.addAction(settings_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", tray_menu)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
        
        self.tray_icon.setToolTip("TodoTips - 待办事项管理")
    
    def setup_hotkeys(self):
        """设置全局快捷键"""
        quick_add_key = self.settings.value('hotkey/quick_add', 'ctrl+shift+a')
        show_window_key = self.settings.value('hotkey/show_window', 'ctrl+shift+t')
        
        self.hotkey_worker = HotkeyWorker(quick_add_key, show_window_key)
        self.hotkey_worker.quick_add_triggered.connect(self.quick_add_from_clipboard)
        self.hotkey_worker.show_window_triggered.connect(self.show_main_window)
        self.hotkey_worker.start()
    
    def show_main_window(self):
        """显示主窗口"""
        self.main_window.show()
        self.main_window.activateWindow()
        self.main_window.raise_()
    
    def quick_add_from_clipboard(self):
        """从剪贴板快速添加待办事项"""
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text and clipboard_text.strip():
                # 添加到当日待办
                todo_id = self.model.add_todo(
                    title=clipboard_text.strip(),
                    category='today'
                )
                
                # 设置提醒（5分钟、15分钟、1小时）
                now = datetime.now()
                self.reminder_manager.add_reminder(
                    todo_id, now + timedelta(minutes=5)
                )
                self.reminder_manager.add_reminder(
                    todo_id, now + timedelta(minutes=15)
                )
                self.reminder_manager.add_reminder(
                    todo_id, now + timedelta(hours=1)
                )
                
                # 显示通知
                self.notification_manager.show_notification(
                    "待办已添加",
                    f"已添加: {clipboard_text[:50]}..."
                )
                
                # 保存数据
                self.model.save_data()
            else:
                self.notification_manager.show_notification(
                    "提示",
                    "剪贴板为空"
                )
        except Exception as e:
            print(f"快速添加错误: {e}")
            self.notification_manager.show_notification(
                "错误",
                f"添加失败: {str(e)}"
            )
    
    def on_reminder(self, todo_id):
        """处理提醒"""
        todo = self.model.get_todo(todo_id)
        if todo and not todo.get('completed', False):
            self.notification_manager.show_notification(
                "待办提醒",
                todo['title'],
                play_sound=True
            )
    
    def update_reminders(self):
        """更新所有提醒"""
        # 清除旧提醒
        self.reminder_manager.clear_all()
        
        # 重新加载所有未完成待办的提醒
        for todo in self.model.get_all_todos():
            if not todo.get('completed', False) and 'reminders' in todo:
                for reminder_time in todo['reminders']:
                    reminder_dt = datetime.fromisoformat(reminder_time)
                    if reminder_dt > datetime.now():
                        self.reminder_manager.add_reminder(
                            todo['id'], reminder_dt
                        )
    
    def show_settings(self):
        """显示设置对话框"""
        from settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.main_window)
        if dialog.exec_():
            # 重启快捷键监听
            self.hotkey_worker.stop()
            self.hotkey_worker.wait()
            self.setup_hotkeys()
    
    def on_tray_activated(self, reason):
        """托盘图标被激活"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_main_window()
    
    def quit_app(self):
        """退出应用"""
        self.hotkey_worker.stop()
        self.hotkey_worker.wait()
        self.model.save_data()
        QMessageBox.information(None, "退出", "应用程序已退出")
        sys.exit(0)
