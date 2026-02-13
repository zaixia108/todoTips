#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NotificationManager - 通知管理器
"""

import os
import sys
from PySide6.QtWidgets import QSystemTrayIcon
from PySide6.QtCore import QObject


class NotificationManager(QObject):
    """通知管理器"""
    
    def __init__(self):
        super().__init__()
        self.sound_enabled = True
    
    def show_notification(self, title, message, play_sound=False):
        """显示系统通知"""
        # 使用系统通知 - 优先使用跨平台的PySide2方式
        try:
            # 尝试使用系统托盘图标显示通知（最可靠的跨平台方式）
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 5000)
            elif sys.platform == 'win32':
                # Windows通知
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(title, message, duration=5, threaded=True)
                except ImportError:
                    # 使用Windows命令行通知 - 使用subprocess安全执行
                    import subprocess
                    # 转义特殊字符以防止注入
                    safe_title = title.replace('"', '""').replace("'", "''")
                    safe_message = message.replace('"', '""').replace("'", "''")
                    cmd = [
                        'powershell', '-Command',
                        f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("{safe_message}", "{safe_title}")'
                    ]
                    subprocess.run(cmd, shell=False, check=False, timeout=5)
            elif sys.platform == 'darwin':
                # macOS通知 - 使用subprocess安全执行
                import subprocess
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(['osascript', '-e', script], check=False, timeout=5)
            else:
                # Linux通知 - 使用subprocess安全执行
                import subprocess
                subprocess.run(['notify-send', title, message], check=False, timeout=5)
        except Exception as e:
            print(f"显示通知失败: {e}")
        
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
                import subprocess
                subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], 
                              check=False, timeout=5)
            else:
                # Linux使用paplay或beep
                import subprocess
                # 尝试paplay，失败则尝试beep
                try:
                    subprocess.run(['paplay', '/usr/share/sounds/freedesktop/stereo/message.oga'],
                                  check=False, timeout=5)
                except (subprocess.SubprocessError, FileNotFoundError):
                    subprocess.run(['beep'], check=False, timeout=5)
        except Exception as e:
            print(f"播放音效错误: {e}")
    
    def set_sound_enabled(self, enabled):
        """设置是否启用音效"""
        self.sound_enabled = enabled
