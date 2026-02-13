#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MainWindow - 主窗口
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTabWidget, QListWidget, QListWidgetItem, QDialog, QLabel,
    QLineEdit, QTextEdit, QComboBox, QCheckBox, QFileDialog,
    QMessageBox, QMenu, QScrollArea
)
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QFont, QAction, QDesktopServices
from datetime import datetime
import json
import tempfile
import os
from llm import summarize_todos


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


class SummaryDialog(QDialog):
    """AI汇总显示对话框"""
    
    def __init__(self, summary_text, parent=None):
        super().__init__(parent)
        self.summary_text = summary_text
        self.setWindowTitle("TodoTips AI 智能汇总")
        self.setMinimumSize(700, 500)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        
        # 时间标签
        time_label = QLabel(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        time_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(time_label)
        
        # 汇总内容显示区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.summary_text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
                line-height: 1.6;
                background-color: white;
            }
        """)
        layout.addWidget(self.text_edit)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 在浏览器中查看按钮
        self.html_button = QPushButton("在浏览器中查看")
        self.html_button.clicked.connect(self.open_in_browser)
        button_layout.addWidget(self.html_button)
        
        # 保存到文件按钮
        self.save_button = QPushButton("保存到文件")
        self.save_button.clicked.connect(self.save_to_file)
        button_layout.addWidget(self.save_button)
        
        # 关闭按钮
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def open_in_browser(self):
        """在浏览器中打开HTML版本"""
        try:
            # 创建HTML内容
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TodoTips AI 智能汇总</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #4CAF50;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .timestamp {{
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }}
        .content {{
            white-space: pre-wrap;
            font-size: 15px;
            line-height: 1.8;
        }}
        .section {{
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 TodoTips AI 智能汇总</h1>
        <div class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        <div class="content">{self._format_html_content(self.summary_text)}</div>
        <div class="footer">Generated by TodoTips AI Assistant</div>
    </div>
</body>
</html>"""
            
            # 创建临时HTML文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_path = f.name
            
            # 在浏览器中打开
            QDesktopServices.openUrl(QUrl.fromLocalFile(temp_path))
            QMessageBox.information(self, "成功", "已在浏览器中打开AI汇总")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开浏览器失败: {str(e)}")
    
    def _format_html_content(self, text):
        """格式化HTML内容"""
        # 简单的文本转HTML，保留换行和段落
        import html
        escaped = html.escape(text)
        # 将连续的换行转换为段落分隔
        escaped = escaped.replace('\n\n', '</p><p class="section">')
        escaped = escaped.replace('\n', '<br>')
        return f'<p class="section">{escaped}</p>'
    
    def save_to_file(self):
        """保存到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存AI汇总", "todos_summary.txt",
            "Text Files (*.txt);;Markdown Files (*.md);;HTML Files (*.html)"
        )
        
        if file_path:
            try:
                if file_path.endswith('.html'):
                    # 保存为HTML
                    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TodoTips AI 智能汇总</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #4CAF50;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .timestamp {{ color: #666; font-size: 14px; margin-bottom: 30px; }}
        .content {{ white-space: pre-wrap; font-size: 15px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 TodoTips AI 智能汇总</h1>
        <div class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        <div class="content">{self._format_html_content(self.summary_text)}</div>
    </div>
</body>
</html>"""
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                else:
                    # 保存为文本/Markdown
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("# TodoTips AI 智能汇总\n\n")
                        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        f.write("---\n\n")
                        f.write(self.summary_text)
                
                QMessageBox.information(self, "成功", f"AI汇总已保存到:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")


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
        
        self.export_button = QPushButton("AI汇总")
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
        """AI汇总待办事项"""
        try:
            # 获取所有待办数据
            export_data = self.model.export_all()
            
            # 使用LLM进行智能汇总
            summary = summarize_todos(export_data)
            
            # 显示汇总对话框
            dialog = SummaryDialog(summary, self)
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"AI汇总失败: {str(e)}")
