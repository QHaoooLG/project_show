#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出行规划功能演示
展示增强的自然语言生成和Markdown导出功能
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def demo_travel_planning():
    """演示出行规划功能"""
    print("🎯 哈基米桌面宠物 - 出行规划功能演示")
    print("=" * 50)
    
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
        
        # 演示1：自然语言解析
        print("\n📝 演示1：自然语言解析")
        print("-" * 30)
        
        user_input = "我想去北京玩3天，预算2000元，喜欢历史和美食"
        print(f"用户输入：{user_input}")
        
        parsed_request = travel_planner.parse_travel_request(user_input)
        print("解析结果：")
        for key, value in parsed_request.items():
            print(f"  {key}: {value}")
        
        # 演示2：生成旅行方案
        print("\n🗺️  演示2：生成旅行方案")
        print("-" * 30)
        
        plans = travel_planner.generate_travel_plan(
            parsed_request['destination'],
            parsed_request['budget'],
            parsed_request['days'],
            parsed_request['preferences']
        )
        
        print(f"成功生成 {len(plans)} 个旅行方案：")
        for i, plan in enumerate(plans, 1):
            print(f"  方案{i}：{plan['title']} - {plan['plan_type']}")
        
        # 演示3：自然语言描述生成
        print("\n📖 演示3：自然语言描述生成")
        print("-" * 30)
        
        selected_plan = plans[0]
        description = travel_planner.generate_natural_language_plan(selected_plan)
        
        print("生成的自然语言描述（前500字符）：")
        print("-" * 40)
        print(description[:500] + "...")
        print("-" * 40)
        
        # 演示4：Markdown导出
        print("\n💾 演示4：Markdown文件导出")
        print("-" * 30)
        
        export_file = "demo_travel_plan.md"
        success = travel_planner.export_plan_to_markdown(selected_plan, export_file)
        
        if success:
            print(f"✅ 成功导出到文件：{export_file}")
            
            # 显示文件内容的前几行
            with open(export_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print("\n文件内容预览（前10行）：")
            print("-" * 40)
            for i, line in enumerate(lines[:10], 1):
                print(f"{i:2d}: {line.rstrip()}")
            print("-" * 40)
            
            # 显示文件信息
            file_size = Path(export_file).stat().st_size
            print(f"文件大小：{file_size} 字节")
            print(f"总行数：{len(lines)} 行")
            
        else:
            print("❌ 导出失败")
        
        # 演示5：多个城市对比
        print("\n🌍 演示5：多个城市方案对比")
        print("-" * 30)
        
        cities = ["北京", "上海", "杭州"]
        for city in cities:
            city_plans = travel_planner.generate_travel_plan(city, 1500, 2, "美食,历史")
            if city_plans:
                plan = city_plans[0]
                print(f"{city}：{plan['title']} - 预计费用 {plan.get('estimated_cost', 0):.0f}元")
        
        print("\n🎉 演示完成！")
        print("\n✨ 功能特点总结：")
        print("1. 🧠 智能自然语言解析 - 从用户输入中提取目的地、预算、天数、偏好")
        print("2. 📋 详细方案生成 - 包含景点、住宿、美食、费用明细")
        print("3. 📝 自然语言描述 - 生成易读的行程说明")
        print("4. 💾 Markdown导出 - 支持导出为格式化的Markdown文件")
        print("5. 🎯 个性化推荐 - 根据用户偏好筛选景点")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    demo_travel_planning()