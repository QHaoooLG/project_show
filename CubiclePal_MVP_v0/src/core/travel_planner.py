#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出行规划模块
负责生成旅行方案
"""

import json
import random
from typing import Dict, List, Any, Tuple
import logging

from utils.database import DatabaseManager

logger = logging.getLogger(__name__)

class TravelPlanner:
    """出行规划器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
        # 静态景点数据（作为备份数据）
        self.attractions_data = {
            "北京": {
                "景点": [
                    {"name": "故宫", "type": "历史", "duration": 4, "cost": 60, "rating": 4.8},
                    {"name": "天安门广场", "type": "历史", "duration": 2, "cost": 0, "rating": 4.6},
                    {"name": "颐和园", "type": "园林", "duration": 3, "cost": 30, "rating": 4.7},
                    {"name": "长城", "type": "历史", "duration": 6, "cost": 45, "rating": 4.9},
                    {"name": "天坛", "type": "历史", "duration": 2, "cost": 15, "rating": 4.5},
                    {"name": "南锣鼓巷", "type": "美食", "duration": 3, "cost": 50, "rating": 4.3},
                    {"name": "798艺术区", "type": "艺术", "duration": 3, "cost": 20, "rating": 4.4},
                ],
                "美食": ["烤鸭", "炸酱面", "豆汁", "驴打滚", "糖葫芦"],
                "住宿": [
                    {"name": "经济型酒店", "price": 200, "rating": 4.0},
                    {"name": "商务酒店", "price": 400, "rating": 4.3},
                    {"name": "豪华酒店", "price": 800, "rating": 4.7},
                ]
            },
            "上海": {
                "景点": [
                    {"name": "外滩", "type": "观光", "duration": 3, "cost": 0, "rating": 4.7},
                    {"name": "东方明珠", "type": "观光", "duration": 2, "cost": 220, "rating": 4.4},
                    {"name": "豫园", "type": "园林", "duration": 2, "cost": 40, "rating": 4.3},
                    {"name": "田子坊", "type": "文化", "duration": 3, "cost": 30, "rating": 4.2},
                    {"name": "南京路", "type": "购物", "duration": 4, "cost": 100, "rating": 4.1},
                    {"name": "迪士尼乐园", "type": "娱乐", "duration": 8, "cost": 399, "rating": 4.6},
                    {"name": "城隍庙", "type": "美食", "duration": 2, "cost": 50, "rating": 4.2},
                ],
                "美食": ["小笼包", "生煎包", "白切鸡", "红烧肉", "糖醋排骨"],
                "住宿": [
                    {"name": "青年旅社", "price": 150, "rating": 3.8},
                    {"name": "商务酒店", "price": 350, "rating": 4.2},
                    {"name": "五星酒店", "price": 1000, "rating": 4.8},
                ]
            },
            "杭州": {
                "景点": [
                    {"name": "西湖", "type": "自然", "duration": 4, "cost": 0, "rating": 4.8},
                    {"name": "灵隐寺", "type": "宗教", "duration": 2, "cost": 45, "rating": 4.5},
                    {"name": "千岛湖", "type": "自然", "duration": 6, "cost": 150, "rating": 4.6},
                    {"name": "宋城", "type": "文化", "duration": 4, "cost": 300, "rating": 4.3},
                    {"name": "河坊街", "type": "美食", "duration": 3, "cost": 60, "rating": 4.2},
                    {"name": "雷峰塔", "type": "历史", "duration": 1, "cost": 40, "rating": 4.1},
                ],
                "美食": ["西湖醋鱼", "龙井虾仁", "叫化鸡", "片儿川", "定胜糕"],
                "住宿": [
                    {"name": "民宿", "price": 180, "rating": 4.1},
                    {"name": "度假酒店", "price": 450, "rating": 4.4},
                    {"name": "奢华酒店", "price": 1200, "rating": 4.9},
                ]
            }
        }
    
    def generate_travel_plan(self, destination: str, budget: float, days: int, 
                           preferences: str = "") -> List[Dict[str, Any]]:
        """
        生成旅行方案
        返回2套不同的方案
        """
        try:
            # 获取目的地数据
            city_data = self.attractions_data.get(destination)
            if not city_data:
                # 如果没有数据，生成通用方案
                return self._generate_generic_plans(destination, budget, days, preferences)
            
            # 根据偏好筛选景点
            filtered_attractions = self._filter_attractions_by_preference(
                city_data["景点"], preferences
            )
            
            # 生成两套不同的方案
            plan1 = self._generate_single_plan(
                destination, filtered_attractions, city_data, budget, days, "经典路线"
            )
            plan2 = self._generate_single_plan(
                destination, filtered_attractions, city_data, budget, days, "深度体验"
            )
            
            return [plan1, plan2]
            
        except Exception as e:
            logger.error(f"生成旅行方案失败: {e}")
            return self._generate_fallback_plans(destination, budget, days)
    
    def _filter_attractions_by_preference(self, attractions: List[Dict], preferences: str) -> List[Dict]:
        """根据偏好筛选景点"""
        if not preferences:
            return attractions
        
        preferences_lower = preferences.lower()
        filtered = []
        
        # 偏好关键词映射
        preference_map = {
            "历史": ["历史", "古迹", "文化", "传统"],
            "自然": ["自然", "风景", "山水", "公园"],
            "美食": ["美食", "小吃", "餐厅", "吃"],
            "购物": ["购物", "商场", "买"],
            "娱乐": ["娱乐", "游乐", "玩"],
            "艺术": ["艺术", "博物馆", "展览"],
        }
        
        # 匹配偏好
        matched_types = []
        for pref_type, keywords in preference_map.items():
            if any(keyword in preferences_lower for keyword in keywords):
                matched_types.append(pref_type.lower())
        
        # 筛选景点
        for attraction in attractions:
            if not matched_types or attraction["type"].lower() in matched_types:
                filtered.append(attraction)
        
        return filtered if filtered else attractions
    
    def _generate_single_plan(self, destination: str, attractions: List[Dict], 
                            city_data: Dict, budget: float, days: int, plan_type: str) -> Dict[str, Any]:
        """生成单个旅行方案"""
        
        # 计算住宿预算（占总预算的40%）
        accommodation_budget = budget * 0.4
        suitable_hotels = [h for h in city_data["住宿"] if h["price"] * days <= accommodation_budget]
        selected_hotel = suitable_hotels[0] if suitable_hotels else city_data["住宿"][0]
        
        # 计算景点预算（占总预算的50%）
        attraction_budget = budget * 0.5
        
        # 选择景点
        if plan_type == "经典路线":
            # 选择评分最高的景点
            selected_attractions = sorted(attractions, key=lambda x: x["rating"], reverse=True)
        else:
            # 深度体验：选择时间较长的景点
            selected_attractions = sorted(attractions, key=lambda x: x["duration"], reverse=True)
        
        # 根据预算和时间筛选景点
        final_attractions = []
        total_cost = 0
        total_time = 0
        max_time_per_day = 8  # 每天最多8小时
        
        for attraction in selected_attractions:
            if (total_cost + attraction["cost"] <= attraction_budget and 
                total_time + attraction["duration"] <= days * max_time_per_day):
                final_attractions.append(attraction)
                total_cost += attraction["cost"]
                total_time += attraction["duration"]
        
        # 生成每日行程
        daily_schedule = self._create_daily_schedule(final_attractions, days)
        
        # 计算总费用
        total_accommodation_cost = selected_hotel["price"] * days
        meal_cost = budget * 0.1  # 餐饮预算10%
        total_estimated_cost = total_cost + total_accommodation_cost + meal_cost
        
        return {
            "title": f"{destination}{days}日{plan_type}",
            "destination": destination,
            "days": days,
            "budget": budget,
            "estimated_cost": total_estimated_cost,
            "plan_type": plan_type,
            "accommodation": selected_hotel,
            "attractions": final_attractions,
            "daily_schedule": daily_schedule,
            "local_food": random.sample(city_data["美食"], min(3, len(city_data["美食"]))),
            "tips": self._generate_travel_tips(destination, plan_type),
            "created_at": "刚刚生成"
        }
    
    def _create_daily_schedule(self, attractions: List[Dict], days: int) -> List[Dict]:
        """创建每日行程安排"""
        daily_schedule = []
        attractions_per_day = len(attractions) // days
        remainder = len(attractions) % days
        
        start_idx = 0
        for day in range(days):
            # 计算当天景点数量
            day_attractions_count = attractions_per_day + (1 if day < remainder else 0)
            day_attractions = attractions[start_idx:start_idx + day_attractions_count]
            start_idx += day_attractions_count
            
            daily_schedule.append({
                "day": day + 1,
                "attractions": day_attractions,
                "total_duration": sum(a["duration"] for a in day_attractions),
                "total_cost": sum(a["cost"] for a in day_attractions)
            })
        
        return daily_schedule
    
    def _generate_travel_tips(self, destination: str, plan_type: str) -> List[str]:
        """生成旅行小贴士"""
        general_tips = [
            "建议提前预订酒店和门票",
            "关注天气预报，准备合适的衣物",
            "下载离线地图，避免迷路",
            "准备充电宝和常用药品",
            "了解当地交通方式"
        ]
        
        city_specific_tips = {
            "北京": ["地铁是最便捷的交通方式", "故宫需要提前网上预约", "春秋季节最适合游览"],
            "上海": ["外滩夜景最美", "地铁覆盖主要景点", "小笼包是必尝美食"],
            "杭州": ["西湖免费开放", "最佳游览时间是春季", "可以租自行车环湖"]
        }
        
        tips = general_tips.copy()
        if destination in city_specific_tips:
            tips.extend(city_specific_tips[destination])
        
        return random.sample(tips, min(5, len(tips)))
    
    def _generate_generic_plans(self, destination: str, budget: float, days: int, preferences: str) -> List[Dict[str, Any]]:
        """生成通用旅行方案（当没有具体城市数据时）"""
        plan1 = {
            "title": f"{destination}{days}日经典游",
            "destination": destination,
            "days": days,
            "budget": budget,
            "estimated_cost": budget * 0.8,
            "plan_type": "经典路线",
            "accommodation": {"name": "当地酒店", "price": budget * 0.4 / days, "rating": 4.0},
            "attractions": [
                {"name": f"{destination}著名景点1", "type": "观光", "duration": 3, "cost": budget * 0.1, "rating": 4.5},
                {"name": f"{destination}著名景点2", "type": "文化", "duration": 2, "cost": budget * 0.05, "rating": 4.3},
            ],
            "daily_schedule": [{"day": i+1, "attractions": [], "total_duration": 6, "total_cost": budget * 0.2} for i in range(days)],
            "local_food": [f"{destination}特色美食"],
            "tips": ["建议提前了解当地文化", "准备好相机记录美好时光"],
            "created_at": "刚刚生成"
        }
        
        plan2 = {**plan1, "title": f"{destination}{days}日深度游", "plan_type": "深度体验"}
        
        return [plan1, plan2]
    
    def _generate_fallback_plans(self, destination: str, budget: float, days: int) -> List[Dict[str, Any]]:
        """生成备用方案"""
        return [{
            "title": f"{destination}旅行方案",
            "destination": destination,
            "days": days,
            "budget": budget,
            "estimated_cost": budget,
            "plan_type": "基础方案",
            "error": "暂时无法生成详细方案，请稍后重试",
            "created_at": "刚刚生成"
        }]
    
    def save_plan(self, plan: Dict[str, Any]) -> int:
        """保存旅行方案"""
        return self.db_manager.save_travel_plan(
            title=plan["title"],
            destination=plan["destination"],
            budget=plan.get("budget", 0),
            days=plan.get("days", 1),
            preferences="",
            plan_data=plan
        )
    
    def get_saved_plans(self) -> List[Dict[str, Any]]:
        """获取已保存的旅行方案"""
        return self.db_manager.get_travel_plans()
    
    def generate_natural_language_plan(self, plan: Dict[str, Any]) -> str:
        """生成自然语言描述的行程规划"""
        try:
            description = f"# {plan['title']}\n\n"
            
            # 基本信息
            description += f"这是一份为期{plan['days']}天的{plan['destination']}旅行计划，"
            description += f"预算为{plan['budget']}元，预计花费{plan.get('estimated_cost', 0):.0f}元。\n\n"
            
            # 住宿推荐
            if 'accommodation' in plan:
                hotel = plan['accommodation']
                description += f"## 🏨 住宿安排\n\n"
                description += f"推荐入住{hotel['name']}，每晚{hotel['price']}元，"
                description += f"评分{hotel['rating']}分，性价比很高。\n\n"
            
            # 每日行程
            if 'daily_schedule' in plan:
                description += f"## 📅 详细行程\n\n"
                for day_info in plan['daily_schedule']:
                    day_num = day_info['day']
                    description += f"### 第{day_num}天\n\n"
                    
                    if day_info['attractions']:
                        description += f"今天安排了{len(day_info['attractions'])}个景点，"
                        description += f"预计游览{day_info['total_duration']}小时，花费{day_info['total_cost']}元。\n\n"
                        
                        for i, attraction in enumerate(day_info['attractions'], 1):
                            description += f"{i}. **{attraction['name']}**\n"
                            description += f"   - 类型：{attraction['type']}\n"
                            description += f"   - 建议游览时间：{attraction['duration']}小时\n"
                            description += f"   - 门票费用：{attraction['cost']}元\n"
                            description += f"   - 游客评分：{attraction['rating']}/5.0\n\n"
                    else:
                        description += "今天可以自由安排，或者休息调整。\n\n"
            
            # 美食推荐
            if 'local_food' in plan:
                description += f"## 🍜 美食推荐\n\n"
                description += f"来到{plan['destination']}，一定要尝试当地特色美食：\n"
                for food in plan['local_food']:
                    description += f"- {food}\n"
                description += "\n"
            
            # 旅行小贴士
            if 'tips' in plan:
                description += f"## 💡 旅行小贴士\n\n"
                for tip in plan['tips']:
                    description += f"- {tip}\n"
                description += "\n"
            
            # 费用明细
            description += f"## 💰 费用预算\n\n"
            if 'accommodation' in plan:
                hotel_cost = plan['accommodation']['price'] * plan['days']
                description += f"- 住宿费用：{hotel_cost}元（{plan['days']}晚）\n"
            
            attraction_cost = sum(day['total_cost'] for day in plan.get('daily_schedule', []))
            description += f"- 景点门票：{attraction_cost}元\n"
            
            meal_cost = plan['budget'] * 0.1
            description += f"- 餐饮预算：{meal_cost:.0f}元\n"
            
            other_cost = plan.get('estimated_cost', 0) - (hotel_cost if 'accommodation' in plan else 0) - attraction_cost - meal_cost
            if other_cost > 0:
                description += f"- 其他费用：{other_cost:.0f}元\n"
            
            description += f"- **总计：{plan.get('estimated_cost', 0):.0f}元**\n\n"
            
            # 结语
            description += f"## 🎯 温馨提示\n\n"
            description += f"这份行程安排仅供参考，您可以根据个人喜好和实际情况进行调整。"
            description += f"祝您在{plan['destination']}度过愉快的{plan['days']}天！\n\n"
            description += f"*行程生成时间：{plan.get('created_at', '未知')}*\n"
            
            return description
            
        except Exception as e:
            logger.error(f"生成自然语言描述失败: {e}")
            return f"# {plan.get('title', '旅行计划')}\n\n生成详细描述时出现错误，请稍后重试。"
    def export_plan_to_markdown(self, plan: Dict[str, Any], file_path: str) -> bool:
        """导出行程计划为Markdown文件"""
        try:
            # 生成自然语言描述
            content = self.generate_natural_language_plan(plan)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"行程计划已导出到: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"导出行程计划失败: {e}")
            return False
    
    def parse_travel_request(self, user_input: str) -> Dict[str, Any]:
        # 简单的正则解析
        import re
        
        result = {
            "destination": "",
            "budget": 1000,
            "days": 2,
            "preferences": ""
        }
        
        # 提取目的地
        cities = ["北京", "上海", "杭州", "广州", "深圳", "成都", "西安", "南京", "苏州", "重庆"]
        for city in cities:
            if city in user_input:
                result["destination"] = city
                break
        
        # 提取预算
        budget_match = re.search(r'(\d+)元', user_input)
        if budget_match:
            result["budget"] = int(budget_match.group(1))
        
        # 提取天数
        days_match = re.search(r'(\d+)天', user_input)
        if days_match:
            result["days"] = int(days_match.group(1))
        
        # 提取偏好
        preferences = []
        if "美食" in user_input or "吃" in user_input:
            preferences.append("美食")
        if "历史" in user_input or "古迹" in user_input:
            preferences.append("历史")
        if "自然" in user_input or "风景" in user_input:
            preferences.append("自然")
        if "购物" in user_input:
            preferences.append("购物")
        
        result["preferences"] = ",".join(preferences)
        
        return result