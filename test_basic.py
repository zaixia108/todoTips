#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TodoTips 基础功能测试
不涉及GUI，只测试核心逻辑
"""

import os
import sys
import json
from datetime import datetime, timedelta

# 导入模块
try:
    from todo_model import TodoModel
    print("✓ todo_model 模块导入成功")
except ImportError as e:
    print(f"✗ todo_model 模块导入失败: {e}")
    sys.exit(1)

def test_todo_model():
    """测试待办事项模型"""
    print("\n测试待办事项模型...")
    
    # 创建临时测试文件
    test_file = '/tmp/test_todos.json'
    if os.path.exists(test_file):
        os.remove(test_file)
    
    model = TodoModel(test_file)
    
    # 测试添加待办
    print("  - 测试添加待办...")
    todo_id1 = model.add_todo("测试任务1", category='today', description='这是测试')
    todo_id2 = model.add_todo("测试任务2", category='week')
    todo_id3 = model.add_todo("测试任务3", category='month')
    
    assert len(model.get_all_todos()) == 3, "添加待办失败"
    print("    ✓ 添加待办成功")
    
    # 测试按类别获取
    print("  - 测试按类别获取...")
    today_todos = model.get_today_todos()
    week_todos = model.get_week_todos()
    month_todos = model.get_month_todos()
    
    assert len(today_todos) == 1, "本日待办数量错误"
    assert len(week_todos) == 1, "本周待办数量错误"
    assert len(month_todos) == 1, "本月待办数量错误"
    print("    ✓ 按类别获取成功")
    
    # 测试完成待办
    print("  - 测试完成待办...")
    model.complete_todo(todo_id1)
    todo = model.get_todo(todo_id1)
    assert todo['completed'] == True, "完成待办失败"
    assert todo['completed_at'] is not None, "完成时间未记录"
    print("    ✓ 完成待办成功")
    
    # 测试添加提醒
    print("  - 测试添加提醒...")
    reminder_time = datetime.now() + timedelta(minutes=5)
    model.add_reminder(todo_id2, reminder_time)
    todo = model.get_todo(todo_id2)
    assert len(todo['reminders']) == 1, "添加提醒失败"
    print("    ✓ 添加提醒成功")
    
    # 测试保存数据
    print("  - 测试保存数据...")
    result = model.save_data()
    assert result == True, "保存数据失败"
    assert os.path.exists(test_file), "数据文件未创建"
    print("    ✓ 保存数据成功")
    
    # 测试加载数据
    print("  - 测试加载数据...")
    model2 = TodoModel(test_file)
    model2.load_data()
    assert len(model2.get_all_todos()) == 3, "加载数据失败"
    print("    ✓ 加载数据成功")
    
    # 测试删除待办
    print("  - 测试删除待办...")
    model.delete_todo(todo_id3)
    assert len(model.get_all_todos()) == 2, "删除待办失败"
    print("    ✓ 删除待办成功")
    
    # 测试导出
    print("  - 测试导出功能...")
    export_data = model.export_all()
    assert 'today' in export_data, "导出数据缺少today"
    assert 'week' in export_data, "导出数据缺少week"
    assert 'month' in export_data, "导出数据缺少month"
    assert export_data['today']['completed'] == 1, "导出统计错误"
    print("    ✓ 导出功能成功")
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("\n✓ 待办事项模型测试全部通过!")

def test_imports():
    """测试所有模块导入"""
    print("\n测试模块导入...")
    
    # 只测试不依赖Qt的核心模块
    modules = [
        'todo_model',
    ]
    
    for module_name in modules:
        try:
            __import__(module_name)
            print(f"  ✓ {module_name} 导入成功")
        except ImportError as e:
            print(f"  ✗ {module_name} 导入失败: {e}")
            return False
    
    # Qt相关模块需要显示环境，跳过实际导入测试
    qt_modules = [
        'reminder_manager',
        'notification_manager', 
        'settings_dialog',
        'main_window',
        'todo_app',
    ]
    
    for module_name in qt_modules:
        # 只检查文件是否存在
        if os.path.exists(f"{module_name}.py"):
            print(f"  ✓ {module_name}.py 文件存在")
        else:
            print(f"  ✗ {module_name}.py 文件缺失")
            return False
    
    print("\n✓ 所有模块文件存在!")
    return True

def test_dependencies():
    """测试依赖包"""
    print("\n测试依赖包...")
    
    dependencies = [
        ('pyperclip', 'pyperclip'),
    ]
    
    all_ok = True
    for display_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"  ✓ {display_name} 已安装")
        except ImportError:
            print(f"  ✗ {display_name} 未安装")
            all_ok = False
    
    # 测试PySide2 (但不实际导入，避免在无显示环境崩溃)
    try:
        import importlib.util
        spec = importlib.util.find_spec('PySide2')
        if spec is not None:
            print(f"  ✓ PySide2 已安装")
        else:
            print(f"  ✗ PySide2 未安装")
            all_ok = False
    except:
        print(f"  ✗ PySide2 未安装")
        all_ok = False
    
    # keyboard可能需要root权限，标记为可选
    try:
        import importlib.util
        spec = importlib.util.find_spec('keyboard')
        if spec is not None:
            print(f"  ✓ keyboard 已安装")
        else:
            print(f"  ⚠ keyboard 未安装 (可选，快捷键功能需要)")
    except:
        print(f"  ⚠ keyboard 未安装 (可选，快捷键功能需要)")
    
    if all_ok:
        print("\n✓ 核心依赖包已安装!")
    else:
        print("\n✗ 部分依赖包未安装，请运行: pip install -r requirements.txt")
    
    return all_ok

def main():
    """主测试函数"""
    print("="*60)
    print("TodoTips 基础功能测试")
    print("="*60)
    
    # 测试依赖
    if not test_dependencies():
        print("\n请先安装依赖包后再运行测试")
        return 1
    
    # 测试导入
    if not test_imports():
        print("\n模块导入失败")
        return 1
    
    # 测试待办模型
    try:
        test_todo_model()
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*60)
    print("所有测试通过! 应用程序核心功能正常。")
    print("="*60)
    print("\n提示: 运行 'python main.py' 启动完整应用程序")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
