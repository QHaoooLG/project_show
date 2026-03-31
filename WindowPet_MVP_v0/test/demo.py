#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈基米桌面宠物 MVP 功能演示脚本
展示核心功能的使用方法
"""

import sys
import time
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def demo_nlp_processor():
    """演示NLP处理器功能"""
    print("\n🧠 === NLP处理器演示 ===")
    
    from ai.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    
    test_inputs = [
        "明天下午2点开会",
        "下周一交报告，重要",
        "提醒我买牛奶",
        "后天上午9点面试"
    ]
    
    for user_input in test_inputs:
        result = nlp.parse_task(user_input)
        print(f"输入: {user_input}")
        print(f"解析: 标题='{result['title']}', 时间='{result['due_time']}', 优先级={result['priority']}")
        print()

def demo_dialogue_generator():
    """演示对话生成器功能"""
    print("\n💬 === 对话生成器演示 ===")
    
    from ai.dialogue_generator import DialogueGenerator
    dialogue = DialogueGenerator()
    
    test_messages = [
        "你好哈基米",
        "我想添加一个任务",
        "我想去旅游",
        "我感觉很累",
        "谢谢你的帮助"
    ]
    
    for message in test_messages:
        response = dialogue.generate_response(message)
        print(f"用户: {message}")
        print(f"哈基米: {response}")
        print()

def demo_task_manager():
    """演示任务管理器功能"""
    print("\n📝 === 任务管理器演示 ===")
    
    from utils.database import DatabaseManager
    from core.task_manager import TaskManager
    from utils.config import ConfigManager
    
    config_manager = ConfigManager()
    db_path = config_manager.get_data_path("demo.db")
    db_manager = DatabaseManager(str(db_path))
    task_manager = TaskManager(db_manager)
    
    # 添加测试任务
    test_tasks = [
        "明天上午10点开会",
        "下周五交项目报告，重要",
        "提醒我买生日礼物"
    ]
    
    print("添加任务:")
    for task_text in test_tasks:
        task_info = task_manager.add_task_from_text(task_text)
        print(f"✅ 已添加: {task_info['title']} (ID: {task_info['id']})")
    
    print("\n当前任务列表:")
    tasks = task_manager.get_pending_tasks()
    for task in tasks:
        print(f"- {task['title']} | 截止: {task['due_time']} | 优先级: {task['priority']}")
    
    print(f"\n任务统计: {task_manager.get_task_statistics()}")

def demo_travel_planner():
    """演示出行规划器功能"""
    print("\n✈️ === 出行规划器演示 ===")
    
    from utils.database import DatabaseManager
    from core.travel_planner import TravelPlanner
    from utils.config import ConfigManager
    
    config_manager = ConfigManager()
    db_path = config_manager.get_data_path("demo.db")
    db_manager = DatabaseManager(str(db_path))
    travel_planner = TravelPlanner(db_manager)
    
    # 解析出行请求
    test_requests = [
        "我想去北京玩2天，预算1000元",
        "上海3日游，喜欢美食",
        "杭州周末游，预算500元"
    ]
    
    for request in test_requests:
        print(f"请求: {request}")
        travel_info = travel_planner.parse_travel_request(request)
        print(f"解析结果: {travel_info}")
        
        if travel_info['destination']:
            print("生成行程方案...")
            plans = travel_planner.generate_travel_plan(
                travel_info['destination'],
                travel_info['budget'],
                travel_info['days'],
                travel_info['preferences']
            )
            
            for i, plan in enumerate(plans):
                print(f"方案{i+1}: {plan['title']}")
                print(f"  预计费用: {plan.get('estimated_cost', 0):.0f}元")
                if 'attractions' in plan:
                    print(f"  景点数量: {len(plan['attractions'])}个")
        print()

def demo_privacy_guard():
    """演示隐私保护器功能"""
    print("\n🔒 === 隐私保护器演示 ===")
    
    from core.privacy_guard import PrivacyGuard
    
    print("隐私保护器功能:")
    print("- 人脸检测监控用户状态")
    print("- 用户离开30秒后自动锁屏")
    print("- 用户返回时自动解锁")
    print("- 支持手动开关隐私模式")
    
    privacy_guard = PrivacyGuard()
    status = privacy_guard.get_status()
    print(f"当前状态: {status}")
    
    print("\n注意: 隐私保护需要摄像头权限，在实际应用中会自动工作")

def main():
    """主演示函数"""
    print("🎯 哈基米桌面宠物 MVP - 功能演示")
    print("=" * 50)
    
    try:
        # 演示各个核心功能
        demo_nlp_processor()
        demo_dialogue_generator()
        demo_task_manager()
        demo_travel_planner()
        demo_privacy_guard()
        
        print("\n🎉 === 演示完成 ===")
        print("所有核心功能都已展示完毕！")
        print("运行 'python start.py' 启动完整的桌面宠物应用")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()