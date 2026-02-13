#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NotificationManager - 通知管理器
"""

import os
import sys
from PySide2.QtWidgets import QSystemTrayIcon
from PySide2.QtCore import QObject


class NotificationManager(QObject):
    """通知管理器"""
    
    def __init__(self):
        super().__init__()
        self.sound_enabled = True
    
    def show_notification(self, title, message, play_sound=False):
        """显示系统通知"""
        # 使用系统通知
        if sys.platform == 'win32':
            # Windows通知
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)
            except ImportError:
                # 如果win10toast不可用，使用QSystemTrayIcon
                icon = QSystemTrayIcon.Information
                QSystemTrayIcon.showMessage(None, title, message, icon, 5000)
        elif sys.platform == 'darwin':
            # macOS通知
            os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')
        else:
            # Linux通知
            os.system(f'notify-send "{title}" "{message}"')
        
        # 播放音效
        if play_sound and self.sound_enabled:
            self.play_sound()
    
    def play_sound(self):
        """播放提醒音效"""
        try:
            # 尝试播放系统声音
            if sys.platform == 'win32':
                import winsound
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            elif sys.platform == 'darwin':
                os.system('afplay /System/Library/Sounds/Glass.aiff')
            else:
                # Linux使用beep或paplay
                os.system('paplay /usr/share/sounds/freedesktop/stereo/message.oga 2>/dev/null || beep')
        except Exception as e:
            print(f"播放音效错误: {e}")
    
    def set_sound_enabled(self, enabled):
        """设置是否启用音效"""
        self.sound_enabled = enabled
