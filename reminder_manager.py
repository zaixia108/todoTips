#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ReminderManager - 提醒管理器
"""

from datetime import datetime
from PySide2.QtCore import QTimer, QObject, Signal


class ReminderManager(QObject):
    """提醒管理器"""
    
    reminder_triggered = Signal(str)  # todo_id
    
    def __init__(self):
        super().__init__()
        self.reminders = {}  # {todo_id: [QTimer, ...]}
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_reminders)
        self.check_timer.start(30000)  # 每30秒检查一次
    
    def add_reminder(self, todo_id, reminder_time):
        """添加提醒"""
        if todo_id not in self.reminders:
            self.reminders[todo_id] = []
        
        # 计算延迟时间（毫秒）
        now = datetime.now()
        delay = (reminder_time - now).total_seconds() * 1000
        
        if delay > 0:
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(lambda: self.trigger_reminder(todo_id))
            timer.start(int(delay))
            self.reminders[todo_id].append(timer)
    
    def trigger_reminder(self, todo_id):
        """触发提醒"""
        self.reminder_triggered.emit(todo_id)
    
    def remove_reminder(self, todo_id):
        """移除待办的所有提醒"""
        if todo_id in self.reminders:
            for timer in self.reminders[todo_id]:
                timer.stop()
            del self.reminders[todo_id]
    
    def clear_all(self):
        """清除所有提醒"""
        for todo_id in list(self.reminders.keys()):
            self.remove_reminder(todo_id)
    
    def check_reminders(self):
        """定期检查提醒"""
        # 这里可以添加额外的检查逻辑
        pass
