#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话生成模块
负责生成智能对话回复和情感交互
"""

import random
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DialogueGenerator:
    """对话生成器"""
    
    def __init__(self):
        # 初始化对话模板
        self.greeting_responses = [
            "你好！我是哈基米，你的专属桌面助手！✨",
            "嗨！哈基米在这里为你服务～有什么需要帮助的吗？",
            "Hello！我是可爱的哈基米，今天过得怎么样？",
            "你好呀！哈基米随时准备为你效劳！💪"
        ]
        
        self.task_responses = [
            "收到！我已经帮你记录了这个任务，到时候会准时提醒你的～",
            "好的！任务已添加，我会在合适的时间提醒你哦！",
            "明白了！这个重要任务我已经记下了，放心交给我吧！",
            "任务记录完成！我会像闹钟一样准时提醒你的～⏰"
        ]
        
        self.travel_responses = [
            "哇！想出去玩呀？告诉我目的地、预算和天数，我来帮你规划完美行程！🎒",
            "旅行计划交给我！说说你想去哪里，预算多少，玩几天？",
            "出行规划是我的强项！快告诉我详细需求，我来制定方案～",
            "太棒了！我最喜欢帮人规划旅行了！说说你的想法吧！✈️"
        ]
        
        self.privacy_responses = [
            "放心！我会像守护神一样保护你的隐私，离开时自动锁屏！🛡️",
            "隐私保护交给我！我会时刻监控，确保你的信息安全～",
            "别担心！我有火眼金睛，会在你离开时自动保护屏幕的！",
            "安全第一！我会24小时守护你的电脑隐私～"
        ]
        
        self.comfort_responses = [
            "辛苦了！要不要休息一下？我陪你聊聊天，放松一下心情～💕",
            "感觉累了吗？来，深呼吸，我在这里陪着你呢！",
            "工作辛苦了！记得劳逸结合哦，我会提醒你休息的～",
            "压力大的时候记得找我聊天！我永远是你的忠实听众～"
        ]
        
        self.praise_responses = [
            "嘿嘿，谢谢夸奖！能帮到你我超开心的～😊",
            "哇！被夸奖了！我会继续努力做你最棒的助手！",
            "谢谢！你的认可是我最大的动力！💪",
            "嘻嘻，你也很棒呢！我们是最佳搭档！"
        ]
        
        self.default_responses = [
            "我在认真听呢！有什么需要帮助的吗？",
            "说得很有道理！还有其他想聊的吗？",
            "嗯嗯，我明白了～继续说说看！",
            "有趣！我很喜欢和你聊天～",
            "我会记住的！还有什么要告诉我的吗？",
            "哈基米在线！随时为你服务～"
        ]
        
        # 情感状态
        self.mood_keywords = {
            'happy': ['开心', '高兴', '快乐', '兴奋', '棒', '好'],
            'sad': ['难过', '伤心', '沮丧', '失落', '郁闷'],
            'tired': ['累', '疲惫', '困', '乏', '疲劳'],
            'stressed': ['压力', '焦虑', '紧张', '忙', '烦'],
            'angry': ['生气', '愤怒', '气', '烦躁', '恼火']
        }
        
        # 时间相关回复
        self.time_responses = {
            'morning': "早上好！新的一天开始了，加油哦！☀️",
            'afternoon': "下午好！工作进展如何？需要我帮忙吗？",
            'evening': "晚上好！今天辛苦了，要早点休息哦！🌙",
            'night': "这么晚还在工作？记得保重身体呀！"
        }
    
    def generate_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """
        生成智能回复
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            生成的回复文本
        """
        try:
            user_input_lower = user_input.lower()
            
            # 检查时间相关回复
            time_response = self._get_time_based_response()
            if time_response and self._is_greeting(user_input_lower):
                return time_response
            
            # 检查情感状态
            mood = self._detect_mood(user_input_lower)
            if mood:
                return self._get_mood_response(mood, user_input)
            
            # 检查功能相关关键词
            if self._contains_keywords(user_input_lower, ['你好', 'hi', 'hello', '哈基米', '在吗']):
                return random.choice(self.greeting_responses)
            
            if self._contains_keywords(user_input_lower, ['任务', '提醒', '记住', '别忘了', '待办']):
                return random.choice(self.task_responses)
            
            if self._contains_keywords(user_input_lower, ['旅游', '出行', '去哪', '玩', '旅行', '行程']):
                return random.choice(self.travel_responses)
            
            if self._contains_keywords(user_input_lower, ['隐私', '保护', '锁屏', '安全']):
                return random.choice(self.privacy_responses)
            
            if self._contains_keywords(user_input_lower, ['谢谢', '感谢', '棒', '厉害', '好棒', '赞']):
                return random.choice(self.praise_responses)
            
            # 默认回复
            return random.choice(self.default_responses)
            
        except Exception as e:
            logger.error(f"对话生成失败: {e}")
            return "哎呀，我有点懵了，能再说一遍吗？"
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """检查文本是否包含关键词"""
        return any(keyword in text for keyword in keywords)
    
    def _is_greeting(self, text: str) -> bool:
        """判断是否为问候语"""
        greeting_words = ['你好', 'hi', 'hello', '早', '晚上好', '下午好']
        return any(word in text for word in greeting_words)
    
    def _detect_mood(self, text: str) -> Optional[str]:
        """检测用户情绪"""
        for mood, keywords in self.mood_keywords.items():
            if any(keyword in text for keyword in keywords):
                return mood
        return None
    
    def _get_mood_response(self, mood: str, user_input: str) -> str:
        """根据情绪生成回复"""
        if mood == 'happy':
            responses = [
                "太好了！看到你开心我也很开心！😊",
                "哇！你的好心情感染到我了！",
                "开心的时候记得分享给我哦～",
                "你开心，我就开心！✨"
            ]
        elif mood == 'sad':
            responses = [
                "别难过，我陪着你呢！有什么想聊的吗？💕",
                "心情不好的时候，记得我永远在这里支持你！",
                "要不要听个笑话？我来逗你开心！",
                "难过的时候抱抱哈基米～一切都会好起来的！"
            ]
        elif mood == 'tired':
            return random.choice(self.comfort_responses)
        elif mood == 'stressed':
            responses = [
                "压力大的时候深呼吸～我来帮你分担一些工作吧！",
                "别着急，一步一步来，我会协助你的！",
                "压力山大？让哈基米来帮你减压！",
                "焦虑的时候记得找我聊天，我会陪着你的～"
            ]
        elif mood == 'angry':
            responses = [
                "生气了吗？要不要跟我说说发生了什么？",
                "别气别气，气坏身体不值得～",
                "愤怒的时候记得深呼吸，我在这里听你倾诉！",
                "有什么让你生气的事吗？说出来会好一些～"
            ]
        else:
            return random.choice(self.default_responses)
        
        return random.choice(responses)
    
    def _get_time_based_response(self) -> Optional[str]:
        """根据时间生成回复"""
        now = datetime.now()
        hour = now.hour
        
        if 5 <= hour < 12:
            return self.time_responses['morning']
        elif 12 <= hour < 18:
            return self.time_responses['afternoon']
        elif 18 <= hour < 22:
            return self.time_responses['evening']
        elif 22 <= hour or hour < 5:
            return self.time_responses['night']
        
        return None
    
    def generate_task_confirmation(self, task_info: Dict[str, Any]) -> str:
        """生成任务确认回复"""
        title = task_info.get('title', '新任务')
        due_time = task_info.get('due_time', '')
        
        if due_time:
            return f"好的！我已经记录了「{title}」，会在 {due_time} 提醒你的～"
        else:
            return f"收到！「{title}」已添加到任务列表中～"
    
    def generate_travel_confirmation(self, travel_info: Dict[str, Any]) -> str:
        """生成出行确认回复"""
        city = travel_info.get('city', '目的地')
        days = travel_info.get('days', '几天')
        budget = travel_info.get('budget', '预算内')
        
        return f"太棒了！{city} {days}日游，{budget}的行程规划正在生成中，请稍等～🎒"
    
    def generate_privacy_alert(self) -> str:
        """生成隐私保护提醒"""
        alerts = [
            "检测到有人靠近！我已经保护好你的屏幕了～🛡️",
            "隐私保护模式启动！屏幕已安全锁定～",
            "有人在看？别担心，我已经帮你锁屏了！",
            "安全第一！屏幕保护已激活～"
        ]
        return random.choice(alerts)
    
    def generate_reminder(self, task_title: str) -> str:
        """生成任务提醒"""
        reminders = [
            f"⏰ 提醒：该处理「{task_title}」了哦！",
            f"🔔 别忘了：「{task_title}」需要你的注意！",
            f"📝 温馨提醒：「{task_title}」的时间到了～",
            f"⚡ 重要提醒：记得完成「{task_title}」！"
        ]
        return random.choice(reminders)