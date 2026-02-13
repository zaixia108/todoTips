#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SettingsDialog - 设置对话框
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QCheckBox,
    QMessageBox
)
from PySide6.QtCore import QSettings


class SettingsDialog(QDialog):
    """设置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings()
        self.setWindowTitle("设置")
        self.setMinimumWidth(450)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        
        # 快捷键设置
        hotkey_group = QGroupBox("快捷键设置")
        hotkey_layout = QVBoxLayout()
        
        # 快速添加快捷键
        quick_add_layout = QHBoxLayout()
        quick_add_layout.addWidget(QLabel("快速添加:"))
        self.quick_add_input = QLineEdit()
        self.quick_add_input.setPlaceholderText("例如: ctrl+shift+a")
        quick_add_layout.addWidget(self.quick_add_input)
        hotkey_layout.addLayout(quick_add_layout)
        
        # 显示窗口快捷键
        show_window_layout = QHBoxLayout()
        show_window_layout.addWidget(QLabel("显示窗口:"))
        self.show_window_input = QLineEdit()
        self.show_window_input.setPlaceholderText("例如: ctrl+shift+t")
        show_window_layout.addWidget(self.show_window_input)
        hotkey_layout.addLayout(show_window_layout)
        
        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)
        
        # 通知设置
        notification_group = QGroupBox("通知设置")
        notification_layout = QVBoxLayout()
        
        self.sound_checkbox = QCheckBox("启用音效")
        notification_layout.addWidget(self.sound_checkbox)
        
        notification_group.setLayout(notification_layout)
        layout.addWidget(notification_group)
        
        # 提示信息
        help_label = QLabel(
            "提示:\n"
            "• 快捷键格式: ctrl+shift+字母\n"
            "• 修改快捷键后需要重启应用生效\n"
            "• 快捷键不能与系统快捷键冲突"
        )
        help_label.setStyleSheet("color: #666; font-size: 11px; padding: 10px;")
        layout.addWidget(help_label)
        
        layout.addStretch()
        
        # 按钮
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_settings(self):
        """加载设置"""
        quick_add = self.settings.value('hotkey/quick_add', 'ctrl+shift+a')
        show_window = self.settings.value('hotkey/show_window', 'ctrl+shift+t')
        sound_enabled = self.settings.value('notification/sound', True, type=bool)
        
        self.quick_add_input.setText(quick_add)
        self.show_window_input.setText(show_window)
        self.sound_checkbox.setChecked(sound_enabled)
    
    def save_settings(self):
        """保存设置"""
        quick_add = self.quick_add_input.text().strip()
        show_window = self.show_window_input.text().strip()
        
        if not quick_add or not show_window:
            QMessageBox.warning(self, "警告", "快捷键不能为空")
            return
        
        if quick_add == show_window:
            QMessageBox.warning(self, "警告", "两个快捷键不能相同")
            return
        
        self.settings.setValue('hotkey/quick_add', quick_add)
        self.settings.setValue('hotkey/show_window', show_window)
        self.settings.setValue('notification/sound', self.sound_checkbox.isChecked())
        
        QMessageBox.information(
            self, "成功", 
            "设置已保存\n请重启应用以使快捷键生效"
        )
        self.accept()
