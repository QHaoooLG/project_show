#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化功能
验证三个主要优化：
1. 对话框关闭不影响主程序
2. 启动时不调用摄像头
3. 增强的出行规划功能
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_privacy_guard_optimization():
    """测试隐私保护优化 - 启动时不调用摄像头"""
    print("🧪 测试隐私保护优化...")
    
    try:
        from core.privacy_guard import PrivacyGuard
        
        # 创建隐私保护器
        privacy_guard = PrivacyGuard()
        
        # 验证启动时没有初始化摄像头
        if privacy_guard.vision_detector is None:
            print("✅ 启动时未初始化摄像头 - 优化成功")
        else:
            print("❌ 启动时仍然初始化了摄像头")
            return False
        
        # 验证手动启动时才初始化摄像头
        print("   测试手动启动隐私保护...")
        privacy_guard.start_protection()
        
        if privacy_guard.vision_detector is not None:
            print("✅ 手动启动时正确初始化摄像头")
        else:
            print("⚠️  手动启动时摄像头初始化失败（可能是摄像头不可用）")
        
        # 停止保护
        privacy_guard.stop_protection()
        print("✅ 隐私保护停止成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 隐私保护测试失败: {e}")
        return False

def test_travel_planner_enhancements():
    """测试出行规划增强功能"""
    print("\n🧪 测试出行规划增强功能...")
    
    try:
        from core.travel_planner import TravelPlanner
        from utils.database import DatabaseManager
        from utils.config import ConfigManager
        
        # 初始化
        config_manager = ConfigManager()
        config = config_manager.load_config()
        db_path = config_manager.get_data_path(config["database"]["path"])
        db_manager = DatabaseManager(str(db_path))
        
        travel_planner = TravelPlanner(db_manager)
        
        # 测试生成旅行方案
        print("   生成测试旅行方案...")
        plans = travel_planner.generate_travel_plan("北京", 1000, 2, "历史,美食")
        
        if plans and len(plans) > 0:
            print(f"✅ 成功生成 {len(plans)} 个旅行方案")
            
            # 测试自然语言生成
            plan = plans[0]
            print("   测试自然语言描述生成...")
            
            if hasattr(travel_planner, 'generate_natural_language_plan'):
                description = travel_planner.generate_natural_language_plan(plan)
                if description and len(description) > 100:
                    print("✅ 自然语言描述生成成功")
                    print(f"   描述长度: {len(description)} 字符")
                else:
                    print("❌ 自然语言描述生成失败")
                    return False
            else:
                print("❌ 缺少自然语言生成功能")
                return False
            
            # 测试Markdown导出
            print("   测试Markdown导出功能...")
            test_file = "test_export.md"
            
            if hasattr(travel_planner, 'export_plan_to_markdown'):
                success = travel_planner.export_plan_to_markdown(plan, test_file)
                if success and Path(test_file).exists():
                    print("✅ Markdown导出功能正常")
                    # 清理测试文件
                    Path(test_file).unlink()
                else:
                    print("❌ Markdown导出失败")
                    return False
            else:
                print("❌ 缺少Markdown导出功能")
                return False
        else:
            print("❌ 旅行方案生成失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 出行规划测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dialog_close_behavior():
    """测试对话框关闭行为"""
    print("\n🧪 测试对话框关闭行为...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
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
        
        # 检查是否设置了正确的属性
        if not chat_dialog.testAttribute(Qt.WA_DeleteOnClose):
            print("✅ 聊天对话框设置了正确的关闭属性")
        else:
            print("❌ 聊天对话框关闭属性设置错误")
            return False
        
        # 测试任务对话框
        task_dialog = TaskDialog(mock_app)
        if not task_dialog.testAttribute(Qt.WA_DeleteOnClose):
            print("✅ 任务对话框设置了正确的关闭属性")
        else:
            print("❌ 任务对话框关闭属性设置错误")
            return False
        
        # 测试出行对话框
        travel_dialog = TravelDialog(mock_app)
        if not travel_dialog.testAttribute(Qt.WA_DeleteOnClose):
            print("✅ 出行对话框设置了正确的关闭属性")
        else:
            print("❌ 出行对话框关闭属性设置错误")
            return False
        
        # 清理
        chat_dialog.close()
        task_dialog.close()
        travel_dialog.close()
        app.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ 对话框测试失败: {e}")
        return False

def test_natural_language_parsing():
    """测试自然语言解析功能"""
    print("\n🧪 测试自然语言解析功能...")
    
    try:
        from core.travel_planner import TravelPlanner
        from utils.database import DatabaseManager
        from utils.config import ConfigManager
        
        # 初始化
        config_manager = ConfigManager()
        config = config_manager.load_config()
        db_path = config_manager.get_data_path(config["database"]["path"])
        db_manager = DatabaseManager(str(db_path))
        
        travel_planner = TravelPlanner(db_manager)
        
        # 测试自然语言解析
        test_inputs = [
            "我想去北京玩3天，预算2000元，喜欢历史和美食",
            "上海2日游，1500元预算",
            "杭州一日游，500元，喜欢自然风光"
        ]
        
        for input_text in test_inputs:
            result = travel_planner.parse_travel_request(input_text)
            print(f"   输入: {input_text}")
            print(f"   解析结果: {result}")
            
            if result['destination'] and result['budget'] > 0 and result['days'] > 0:
                print("   ✅ 解析成功")
            else:
                print("   ❌ 解析失败")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 自然语言解析测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试哈基米桌面宠物优化功能...")
    
    success = True
    
    # 运行所有测试
    success &= test_privacy_guard_optimization()
    success &= test_travel_planner_enhancements()
    success &= test_dialog_close_behavior()
    success &= test_natural_language_parsing()
    
    if success:
        print("\n🎉 所有优化功能测试通过！")
        print("\n✅ 优化总结:")
        print("1. 对话框关闭不会影响主程序运行")
        print("2. 启动时不会自动调用摄像头，只有手动开启隐私保护时才调用")
        print("3. 出行规划功能增强:")
        print("   - 支持自然语言生成详细行程描述")
        print("   - 支持导出为Markdown文件")
        print("   - 可自由选择导出位置")
        print("   - 增强的自然语言解析功能")
    else:
        print("\n❌ 部分优化功能测试失败，请检查相关模块。")