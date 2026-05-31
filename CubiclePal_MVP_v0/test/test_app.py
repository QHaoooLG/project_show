#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试应用启动脚本
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_modules():
    """测试各个模块"""
    print("=== 哈基米桌面宠物 MVP 模块测试 ===")
    
    try:
        # 测试配置管理器
        from utils.config import ConfigManager
        config_manager = ConfigManager()
        config = config_manager.load_config()
        print("✅ 配置管理器测试通过")
        
        # 测试数据库管理器
        from utils.database import DatabaseManager
        db_path = config_manager.get_data_path("test.db")
        db_manager = DatabaseManager(str(db_path))
        print("✅ 数据库管理器测试通过")
        
        # 测试NLP处理器
        from ai.nlp_processor import NLPProcessor
        nlp = NLPProcessor()
        result = nlp.parse_task("明天下午2点开会")
        print(f"✅ NLP处理器测试通过: {result['title']}")
        
        # 测试对话生成器
        from ai.dialogue_generator import DialogueGenerator
        dialogue = DialogueGenerator()
        response = dialogue.generate_response("你好")
        print(f"✅ 对话生成器测试通过: {response}")
        
        # 测试任务管理器
        from core.task_manager import TaskManager
        task_manager = TaskManager(db_manager)
        task_info = task_manager.add_task_from_text("测试任务：明天上午9点开会")
        print(f"✅ 任务管理器测试通过: 任务ID {task_info['id']}")
        
        # 测试出行规划器
        from core.travel_planner import TravelPlanner
        travel_planner = TravelPlanner(db_manager)
        travel_info = travel_planner.parse_travel_request("我想去北京玩2天，预算1000元")
        print(f"✅ 出行规划器测试通过: {travel_info}")
        
        print("\n🎉 所有核心模块测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui():
    """测试UI模块（需要图形界面）"""
    try:
        # 检查PyQt5是否可用
        try:
            from PyQt5.QtWidgets import QApplication
            print("✅ PyQt5 可用")
        except ImportError:
            try:
                from PySide2.QtWidgets import QApplication
                print("✅ PySide2 可用")
            except ImportError:
                print("❌ 未安装 PyQt5 或 PySide2")
                return False
        
        print("✅ UI框架测试通过")
        return True
        
    except Exception as e:
        print(f"❌ UI测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试哈基米桌面宠物 MVP...")
    
    # 测试核心模块
    if test_modules():
        print("\n核心功能测试完成！")
        
        # 测试UI（可选）
        if len(sys.argv) > 1 and sys.argv[1] == "--ui":
            test_ui()
        
        print("\n🚀 哈基米桌面宠物 MVP 准备就绪！")
        print("运行 'python main.py' 启动完整应用")
    else:
        print("\n❌ 测试失败，请检查错误信息")
        sys.exit(1)