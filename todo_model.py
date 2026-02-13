#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TodoModel - 待办事项数据模型
"""

import json
import os
from datetime import datetime, timedelta
import uuid


class TodoModel:
    """待办事项数据模型"""
    
    def __init__(self, data_file='todos.json'):
        self.data_file = data_file
        self.todos = []
    
    def add_todo(self, title, category='today', description='', due_date=None):
        """添加待办事项"""
        todo = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'category': category,
            'created_at': datetime.now().isoformat(),
            'due_date': due_date.isoformat() if due_date else None,
            'completed': False,
            'completed_at': None,
            'reminders': []
        }
        self.todos.append(todo)
        return todo['id']
    
    def get_todo(self, todo_id):
        """获取待办事项"""
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo
        return None
    
    def update_todo(self, todo_id, **kwargs):
        """更新待办事项"""
        todo = self.get_todo(todo_id)
        if todo:
            for key, value in kwargs.items():
                if key in todo:
                    todo[key] = value
            return True
        return False
    
    def delete_todo(self, todo_id):
        """删除待办事项"""
        self.todos = [t for t in self.todos if t['id'] != todo_id]
    
    def complete_todo(self, todo_id):
        """完成待办事项"""
        todo = self.get_todo(todo_id)
        if todo:
            todo['completed'] = True
            todo['completed_at'] = datetime.now().isoformat()
            return True
        return False
    
    def get_todos_by_category(self, category):
        """按类别获取待办事项"""
        return [t for t in self.todos if t['category'] == category]
    
    def get_today_todos(self):
        """获取今日待办"""
        return self.get_todos_by_category('today')
    
    def get_week_todos(self):
        """获取本周待办"""
        return self.get_todos_by_category('week')
    
    def get_month_todos(self):
        """获取本月待办"""
        return self.get_todos_by_category('month')
    
    def get_all_todos(self):
        """获取所有待办事项"""
        return self.todos
    
    def add_reminder(self, todo_id, reminder_time):
        """为待办添加提醒时间"""
        todo = self.get_todo(todo_id)
        if todo:
            if 'reminders' not in todo:
                todo['reminders'] = []
            todo['reminders'].append(reminder_time.isoformat())
            return True
        return False
    
    def save_data(self):
        """保存数据到文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据错误: {e}")
            return False
    
    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
                return True
            except Exception as e:
                print(f"加载数据错误: {e}")
                return False
        return False
    
    def export_category(self, category):
        """导出指定类别的待办事项"""
        todos = self.get_todos_by_category(category)
        export_data = {
            'category': category,
            'export_time': datetime.now().isoformat(),
            'total': len(todos),
            'completed': len([t for t in todos if t.get('completed', False)]),
            'todos': todos
        }
        return export_data
    
    def export_all(self):
        """导出所有待办事项"""
        return {
            'today': self.export_category('today'),
            'week': self.export_category('week'),
            'month': self.export_category('month')
        }
