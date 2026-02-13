# 开发指南

## 项目结构

```
todoTips/
├── main.py                    # 应用程序入口
├── todo_app.py                # 主应用程序类，管理托盘和快捷键
├── todo_model.py              # 数据模型，处理待办事项的CRUD
├── main_window.py             # 主窗口UI，包含三个标签页
├── settings_dialog.py         # 设置对话框
├── reminder_manager.py        # 提醒管理器
├── notification_manager.py    # 通知管理器
├── requirements.txt           # 依赖列表
├── setup.py                   # 安装配置
├── README.md                  # 项目说明
├── QUICKSTART.md              # 快速开始指南
├── DEVELOPMENT.md             # 本文件
├── test_basic.py              # 基础功能测试
└── todos.json                 # 数据文件（运行时生成）
```

## 架构设计

### 模块职责

1. **main.py**
   - 应用程序入口点
   - 初始化QApplication
   - 创建TodoApplication实例

2. **todo_app.py**
   - 主应用逻辑
   - 系统托盘管理
   - 全局快捷键监听
   - 协调各个组件

3. **todo_model.py**
   - 数据模型和业务逻辑
   - JSON文件持久化
   - 待办事项CRUD操作
   - 数据导出功能

4. **main_window.py**
   - 主窗口UI
   - 三个标签页（本日/本周/本月）
   - 待办列表显示
   - 用户交互处理

5. **reminder_manager.py**
   - 管理所有提醒定时器
   - 触发提醒信号

6. **notification_manager.py**
   - 跨平台系统通知
   - 音效播放

7. **settings_dialog.py**
   - 快捷键配置
   - 通知设置

## 数据流

```
用户操作 → UI组件 → TodoModel → JSON文件
                 ↓
            ReminderManager
                 ↓
         NotificationManager
```

## 扩展开发

### 添加新功能

1. **添加新的待办属性**
   - 修改 `todo_model.py` 中的 `add_todo` 方法
   - 更新 `main_window.py` 中的UI
   - 更新导出功能

2. **添加新的提醒模式**
   - 修改快速添加逻辑
   - 在 `todo_app.py` 的 `quick_add_from_clipboard` 中添加

3. **自定义样式**
   - 修改 `main_window.py` 中的 `apply_stylesheet` 方法
   - 使用Qt样式表语法

4. **添加新的板块**
   - 在 `main_window.py` 中添加新标签页
   - 在 `todo_model.py` 中添加对应的getter方法

### 调试技巧

1. **查看数据文件**
   ```bash
   cat todos.json | python -m json.tool
   ```

2. **测试核心功能**
   ```bash
   python test_basic.py
   ```

3. **查看日志**
   - 应用会在终端输出调试信息
   - 查看异常堆栈

## 打包发布

### 使用PyInstaller打包

```bash
pip install pyinstaller

# Windows
pyinstaller --onefile --windowed --icon=icon.ico main.py

# Linux
pyinstaller --onefile --windowed main.py

# macOS
pyinstaller --onefile --windowed --icon=icon.icns main.py
```

### 创建安装包

```bash
# 使用setup.py
python setup.py sdist bdist_wheel

# 安装
pip install dist/TodoTips-1.0.0-py3-none-any.whl
```

## 贡献指南

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 代码规范

- 遵循PEP 8
- 使用有意义的变量名
- 添加必要的注释和文档字符串
- 保持函数简洁

## 测试

运行测试：
```bash
python test_basic.py
```

## 已知问题

1. **Linux快捷键权限**
   - 全局快捷键在Linux上可能需要sudo权限
   - 解决方案：使用sudo运行或配置udev规则

2. **macOS通知权限**
   - 首次运行需要授予通知权限
   - 在系统偏好设置中配置

3. **Windows防火墙**
   - 可能会提示防火墙警告
   - 允许即可

## 路线图

- [ ] 添加任务优先级
- [ ] 支持子任务
- [ ] 添加标签系统
- [ ] 支持任务搜索
- [ ] 添加统计图表
- [ ] 支持云同步
- [ ] 添加番茄钟功能
- [ ] 支持主题切换
- [ ] 添加快捷键冲突检测
- [ ] 支持数据导入

## 许可证

MIT License - 查看 LICENSE 文件了解详情
