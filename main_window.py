#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MainWindow - 主窗口
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTabWidget, QListWidget, QListWidgetItem, QDialog, QLabel,
    QLineEdit, QTextEdit, QComboBox, QCheckBox, QFileDialog,
    QMessageBox, QMenu
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QAction
from datetime import datetime
import json


class TodoItemWidget(QWidget):
    """待办事项列表项"""
    
    def __init__(self, todo, parent=None):
        super().__init__(parent)
        self.todo = todo
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 完成复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.todo.get('completed', False))
        layout.addWidget(self.checkbox)
        
        # 标题
        self.title_label = QLabel(self.todo['title'])
        self.title_label.setWordWrap(True)
        font = QFont()
        font.setPointSize(10)
        self.title_label.setFont(font)
        if self.todo.get('completed', False):
            self.title_label.setStyleSheet("color: gray; text-decoration: line-through;")
        layout.addWidget(self.title_label, 1)
        
        # 时间标签
        created_time = datetime.fromisoformat(self.todo['created_at'])
        time_str = created_time.strftime('%H:%M')
        self.time_label = QLabel(time_str)
        self.time_label.setStyleSheet("color: #888;")
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)


class AddTodoDialog(QDialog):
    """添加待办事项对话框"""
    
    def __init__(self, parent=None, category='today'):
        super().__init__(parent)
        self.category = category
        self.setWindowTitle("添加待办事项")
        self.setMinimumWidth(400)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        
        # 标题
        title_label = QLabel("标题:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("输入待办事项标题...")
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        
        # 描述
        desc_label = QLabel("描述 (可选):")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("输入详细描述...")
        self.desc_input.setMaximumHeight(100)
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_input)
        
        # 类别
        category_label = QLabel("类别:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["本日", "本周", "本月"])
        if self.category == 'today':
            self.category_combo.setCurrentIndex(0)
        elif self.category == 'week':
            self.category_combo.setCurrentIndex(1)
        elif self.category == 'month':
            self.category_combo.setCurrentIndex(2)
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)
        
        # 按钮
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_todo_data(self):
        """获取待办数据"""
        category_map = {0: 'today', 1: 'week', 2: 'month'}
        return {
            'title': self.title_input.text(),
            'description': self.desc_input.toPlainText(),
            'category': category_map[self.category_combo.currentIndex()]
        }


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle("TodoTips - 待办事项管理")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.apply_stylesheet()
        self.refresh_all_lists()
    
    def setup_ui(self):
        """设置UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # 顶部按钮栏
        top_layout = QHBoxLayout()
        
        self.add_button = QPushButton("+ 添加待办")
        self.add_button.clicked.connect(self.add_todo)
        top_layout.addWidget(self.add_button)
        
        self.refresh_button = QPushButton("刷新")
        self.refresh_button.clicked.connect(self.refresh_all_lists)
        top_layout.addWidget(self.refresh_button)
        
        self.export_button = QPushButton("导出")
        self.export_button.clicked.connect(self.export_todos)
        top_layout.addWidget(self.export_button)
        
        top_layout.addStretch()
        
        layout.addLayout(top_layout)
        
        # 标签页
        self.tab_widget = QTabWidget()
        
        # 本日标签
        self.today_list = QListWidget()
        self.today_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.today_list.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, 'today')
        )
        self.tab_widget.addTab(self.today_list, "本日")
        
        # 本周标签
        self.week_list = QListWidget()
        self.week_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.week_list.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, 'week')
        )
        self.tab_widget.addTab(self.week_list, "本周")
        
        # 本月标签
        self.month_list = QListWidget()
        self.month_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.month_list.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, 'month')
        )
        self.tab_widget.addTab(self.month_list, "本月")
        
        layout.addWidget(self.tab_widget)
        
        central_widget.setLayout(layout)
    
    def apply_stylesheet(self):
        """应用样式表"""
        stylesheet = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-size: 14px;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QTabWidget::pane {
            border: 1px solid #ddd;
            background-color: white;
            border-radius: 4px;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            color: #333;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        
        QTabBar::tab:selected {
            background-color: white;
            color: #4CAF50;
            font-weight: bold;
        }
        
        QTabBar::tab:hover {
            background-color: #f0f0f0;
        }
        
        QListWidget {
            background-color: white;
            border: none;
            font-size: 13px;
        }
        
        QListWidget::item {
            border-bottom: 1px solid #eee;
            padding: 5px;
        }
        
        QListWidget::item:hover {
            background-color: #f9f9f9;
        }
        
        QListWidget::item:selected {
            background-color: #e3f2fd;
            color: #333;
        }
        
        QLineEdit, QTextEdit {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            font-size: 13px;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #4CAF50;
        }
        
        QComboBox {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 6px;
            font-size: 13px;
        }
        
        QLabel {
            font-size: 13px;
            color: #333;
        }
        """
        self.setStyleSheet(stylesheet)
    
    def add_todo(self):
        """添加待办事项"""
        current_tab = self.tab_widget.currentIndex()
        category = ['today', 'week', 'month'][current_tab]
        
        dialog = AddTodoDialog(self, category)
        if dialog.exec_():
            data = dialog.get_todo_data()
            if data['title']:
                self.model.add_todo(
                    title=data['title'],
                    category=data['category'],
                    description=data['description']
                )
                self.model.save_data()
                self.refresh_all_lists()
    
    def refresh_all_lists(self):
        """刷新所有列表"""
        self.refresh_list(self.today_list, self.model.get_today_todos())
        self.refresh_list(self.week_list, self.model.get_week_todos())
        self.refresh_list(self.month_list, self.model.get_month_todos())
    
    def refresh_list(self, list_widget, todos):
        """刷新列表"""
        list_widget.clear()
        for todo in todos:
            item = QListWidgetItem()
            widget = TodoItemWidget(todo)
            widget.checkbox.stateChanged.connect(
                lambda state, t=todo: self.on_todo_checked(t, state)
            )
            item.setSizeHint(widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)
    
    def on_todo_checked(self, todo, state):
        """待办事项复选框状态改变"""
        if state == Qt.Checked:
            self.model.complete_todo(todo['id'])
        else:
            self.model.update_todo(todo['id'], completed=False, completed_at=None)
        self.model.save_data()
        self.refresh_all_lists()
    
    def show_context_menu(self, pos, category):
        """显示右键菜单"""
        list_widget = getattr(self, f'{category}_list')
        item = list_widget.itemAt(pos)
        if item:
            menu = QMenu()
            
            delete_action = QAction("删除", self)
            delete_action.triggered.connect(
                lambda: self.delete_todo(list_widget, item)
            )
            menu.addAction(delete_action)
            
            menu.exec_(list_widget.mapToGlobal(pos))
    
    def delete_todo(self, list_widget, item):
        """删除待办事项"""
        widget = list_widget.itemWidget(item)
        if widget:
            reply = QMessageBox.question(
                self, '确认删除', 
                f'确定要删除"{widget.todo["title"]}"吗？',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.model.delete_todo(widget.todo['id'])
                self.model.save_data()
                self.refresh_all_lists()
    
    def export_todos(self):
        """导出待办事项"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出待办事项", "todos_export.json",
            "JSON Files (*.json);;Text Files (*.txt)"
        )
        
        if file_path:
            try:
                export_data = self.model.export_all()
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "成功", f"待办事项已导出到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
