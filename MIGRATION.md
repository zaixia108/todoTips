# PySide2 到 PySide6 迁移指南

## 概述

本文档记录了 TodoTips 项目从 PySide2 迁移到 PySide6 的变更。

## 为什么要迁移？

- **更新的Qt版本**: PySide6 基于 Qt 6，提供了更好的性能和新特性
- **更好的Python支持**: 更好地支持现代Python版本
- **长期支持**: Qt 6 是未来的主要版本
- **改进的API**: 更一致和现代化的API设计

## 主要变更

### 1. 依赖变更

**之前 (PySide2)**:
```
PySide2>=5.15.0
```

**现在 (PySide6)**:
```
PySide6>=6.0.0
```

### 2. 导入变更

#### QAction 位置变更

**之前 (PySide2)**:
```python
from PySide2.QtWidgets import QAction
```

**现在 (PySide6)**:
```python
from PySide6.QtGui import QAction
```

#### 其他导入保持一致

```python
# QtWidgets 模块
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSystemTrayIcon, etc.
)

# QtCore 模块
from PySide6.QtCore import (
    Qt, QTimer, QThread, Signal, QSettings, etc.
)

# QtGui 模块
from PySide6.QtGui import (
    QIcon, QFont, QAction, etc.
)
```

### 3. API 变更

#### 应用程序执行

**之前 (PySide2)**:
```python
sys.exit(app.exec_())
```

**现在 (PySide6)**:
```python
sys.exit(app.exec())
```

#### 高DPI缩放

**之前 (PySide2)**:
```python
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
```

**现在 (PySide6)**:
```python
QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
```

## 受影响的文件

### Python 模块

1. `main.py` - 应用入口，更新高DPI设置和exec方法
2. `todo_app.py` - QAction导入位置变更
3. `main_window.py` - QAction导入位置变更
4. `notification_manager.py` - 导入和注释更新
5. `reminder_manager.py` - 导入更新
6. `settings_dialog.py` - 导入更新
7. `test_basic.py` - 依赖检查更新

### 配置文件

1. `requirements.txt` - 依赖版本更新
2. `setup.py` - 安装配置更新

### 脚本文件

1. `start.sh` - 依赖检查更新
2. `start.bat` - 依赖检查更新

### 文档文件

1. `README.md` - 所有PySide2引用更新
2. `SUMMARY.md` - 所有PySide2引用更新

## 兼容性

### Python 版本支持

- PySide6 需要 Python 3.6 或更高版本
- 推荐使用 Python 3.8+ 以获得最佳兼容性

### 操作系统支持

- Windows 7+ (推荐 Windows 10+)
- macOS 10.13+ (推荐 macOS 11+)
- Linux (所有现代发行版)

## 安装说明

### 卸载旧版本 (可选)

```bash
pip uninstall PySide2
```

### 安装新版本

```bash
pip install -r requirements.txt
```

或直接安装：

```bash
pip install PySide6>=6.0.0
```

## 测试

运行测试以验证迁移：

```bash
python test_basic.py
```

预期输出应显示 PySide6 已安装并且所有测试通过。

## 已知问题

### Linux 快捷键权限

迁移不影响 keyboard 库的权限要求，Linux 系统仍可能需要 sudo 权限。

### macOS 通知权限

迁移不影响通知权限设置，首次运行仍需授予权限。

## 回退指南

如果需要回退到 PySide2：

1. 恢复 requirements.txt:
   ```
   PySide2>=5.15.0
   ```

2. 恢复所有导入语句（将 PySide6 改回 PySide2）

3. 恢复 main.py 中的高DPI设置和 exec_() 调用

4. 重新安装依赖:
   ```bash
   pip uninstall PySide6
   pip install -r requirements.txt
   ```

## 参考资料

- [PySide6 官方文档](https://doc.qt.io/qtforpython-6/)
- [Qt 6 移植指南](https://doc.qt.io/qt-6/portingguide.html)
- [PySide2 到 PySide6 迁移指南](https://doc.qt.io/qtforpython-6/gettingstarted/porting_from2.html)

## 结论

迁移已成功完成，所有功能保持不变。PySide6 提供了更好的性能和未来支持。

---

**迁移日期**: 2026-02-13  
**版本**: 1.0.0 → 1.1.0
