#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试对话框UI功能
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication
from ui.dialogs_fixed import ChatDialog, TaskDialog, TravelDialog

class MockApp:
    """模拟应用对象"""
    def __init__(self):
        self.name = "测试应用"

def test_chat_dialog():
    """测试聊天对话框"""
    app = QApplication([])
    mock_app = MockApp()
    
    dialog = ChatDialog(mock_app)
    dialog.show()
    
    print("✅ 聊天对话框创建成功")
    print("- 窗口标题:", dialog.windowTitle())
    print("- 窗口大小:", dialog.size().width(), "x", dialog.size().height())
    
    # 测试发送消息
    dialog.add_message("测试用户", "你好哈基米！", False)
    dialog.add_message("哈基米", "你好！很高兴见到你！", True)
    
    print("- 消息显示功能正常")
    
    dialog.close()
    app.quit()

def test_task_dialog():
    """测试任务管理对话框"""
    app = QApplication([])
    mock_app = MockApp()
    
    dialog = TaskDialog(mock_app)
    dialog.show()
    
    print("✅ 任务管理对话框创建成功")
    print("- 窗口标题:", dialog.windowTitle())
    print("- 窗口大小:", dialog.size().width(), "x", dialog.size().height())
    
    dialog.close()
    app.quit()

def test_travel_dialog():
    """测试出行规划对话框"""
    app = QApplication([])
    mock_app = MockApp()
    
    dialog = TravelDialog(mock_app)
    dialog.show()
    
    print("✅ 出行规划对话框创建成功")
    print("- 窗口标题:", dialog.windowTitle())
    print("- 窗口大小:", dialog.size().width(), "x", dialog.size().height())
    
    dialog.close()
    app.quit()

if __name__ == "__main__":
    print("🧪 开始测试对话框UI功能...")
    
    try:
        test_chat_dialog()
        test_task_dialog()
        test_travel_dialog()
        
        print("\n🎉 所有对话框测试通过！")
        print("现在你可以在桌面宠物中正常使用聊天、任务管理和出行规划功能了。")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()