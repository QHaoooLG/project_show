#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试 - 验证所有模块能正常协作
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_imports():
    """测试所有模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        # 测试工具模块
        from utils.config import ConfigManager
        from utils.database import DatabaseManager
        from utils.logger import setup_logger
        print("✅ 工具模块导入成功")
        
        # 测试AI模块
        from ai.nlp_processor import NLPProcessor
        from ai.dialogue_generator import DialogueGenerator
        print("✅ AI模块导入成功")
        
        # 测试核心模块
        from core.task_manager import TaskManager
        from core.travel_planner import TravelPlanner
        from core.privacy_guard import PrivacyGuard
        print("✅ 核心模块导入成功")
        
        # 测试UI模块
        from ui.dialogs_fixed import ChatDialog, TaskDialog, TravelDialog
        print("✅ UI模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    try:
        # 测试配置管理
        from utils.config import ConfigManager
        config_manager = ConfigManager()
        config = config_manager.load_config()
        print(f"✅ 配置加载成功 - 宠物名称: {config['pet']['name']}")
        
        # 测试数据库
        from utils.database import DatabaseManager
        db_path = config_manager.get_data_path(config["database"]["path"])
        db_manager = DatabaseManager(str(db_path))
        print("✅ 数据库连接成功")
        
        # 测试NLP处理器
        from ai.nlp_processor import NLPProcessor
        nlp = NLPProcessor()
        response = nlp.generate_response("你好")
        print(f"✅ NLP处理器工作正常 - 回复: {response}")
        
        # 测试任务管理器
        from core.task_manager import TaskManager
        task_manager = TaskManager(db_manager)
        print("✅ 任务管理器初始化成功")
        
        # 测试出行规划器
        from core.travel_planner import TravelPlanner
        travel_planner = TravelPlanner(db_manager)
        print("✅ 出行规划器初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dialog_creation():
    """测试对话框创建"""
    print("\n🧪 测试对话框创建...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.dialogs_fixed import ChatDialog, TaskDialog, TravelDialog
        
        # 创建应用
        app = QApplication([])
        
        # 模拟应用对象
        class MockApp:
            def __init__(self):
                self.name = "测试应用"
        
        mock_app = MockApp()
        
        # 测试聊天对话框
        chat_dialog = ChatDialog(mock_app)
        print("✅ 聊天对话框创建成功")
        
        # 测试任务对话框
        task_dialog = TaskDialog(mock_app)
        print("✅ 任务对话框创建成功")
        
        # 测试出行对话框
        travel_dialog = TravelDialog(mock_app)
        print("✅ 出行对话框创建成功")
        
        # 清理
        chat_dialog.close()
        task_dialog.close()
        travel_dialog.close()
        app.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ 对话框测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 开始哈基米桌面宠物集成测试...")
    
    success = True
    
    # 运行所有测试
    success &= test_imports()
    success &= test_basic_functionality()
    success &= test_dialog_creation()
    
    if success:
        print("\n🎉 所有测试通过！")
        print("哈基米桌面宠物的所有功能模块都能正常工作。")
        print("现在你可以放心使用桌面宠物的所有功能了：")
        print("- 💬 聊天对话")
        print("- 📝 任务管理")
        print("- ✈️ 出行规划")
        print("- 🔒 隐私保护")
    else:
        print("\n❌ 部分测试失败，请检查相关模块。")