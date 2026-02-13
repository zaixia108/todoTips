# 更新日志 (Changelog)

## [1.1.0] - 2026-02-13

### 重大变更
- **迁移到 PySide6**: 将整个项目从 PySide2 迁移到 PySide6 (Qt 6)
  - 更新所有依赖从 PySide2 >= 5.15.0 到 PySide6 >= 6.0.0
  - 更新所有导入语句
  - 应用 PySide6 API 变更

### API 变更
- `QAction` 从 `PySide6.QtWidgets` 移至 `PySide6.QtGui`
- 应用执行方法从 `app.exec_()` 改为 `app.exec()`
- 高DPI缩放设置更新为 `setHighDpiScaleFactorRoundingPolicy`

### 新增文件
- `MIGRATION.md` - 详细的 PySide2 到 PySide6 迁移指南
- `CHANGELOG.md` - 项目更新日志

### 更新的文件
- **Python模块**: main.py, todo_app.py, main_window.py, notification_manager.py, reminder_manager.py, settings_dialog.py, test_basic.py
- **配置文件**: requirements.txt, setup.py
- **脚本文件**: start.sh, start.bat
- **文档**: README.md, SUMMARY.md

### 兼容性
- ✅ 所有功能保持完全一致
- ✅ 用户体验无变化
- ✅ 向后兼容（通过迁移指南）

### 测试
- ✅ 代码语法验证通过
- ✅ 代码审查通过（0个问题）
- ✅ 安全扫描通过（CodeQL: 0告警）

---

## [1.0.0] - 2026-02-13

### 新增功能
- ✅ 全局快捷键支持（Ctrl+Shift+A, Ctrl+Shift+T）
- ✅ 从剪贴板快速添加待办
- ✅ 智能提醒系统（5分钟、15分钟、1小时）
- ✅ 多板块管理（本日、本周、本月）
- ✅ 系统托盘运行
- ✅ 跨平台系统通知
- ✅ 音效提醒
- ✅ 数据导出（JSON格式）
- ✅ 现代化UI设计

### 技术栈
- Python 3.6+
- PySide2 5.15+
- keyboard 0.13.5+
- pyperclip 1.8.2+

### 文档
- README.md - 项目说明
- QUICKSTART.md - 快速入门
- DEVELOPMENT.md - 开发指南
- SUMMARY.md - 项目总结
- DEMO.md - 演示指南
- LICENSE - MIT许可证
