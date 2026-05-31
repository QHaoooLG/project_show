#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自然语言处理模块
负责任务解析和对话生成
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class NLPProcessor:
    """自然语言处理器"""
    
    def __init__(self):
        # 时间关键词映射
        self.time_patterns = {
            r'明天': 1,
            r'后天': 2,
            r'大后天': 3,
            r'下周': 7,
            r'(\d+)天后': lambda m: int(m.group(1)),
            r'(\d+)小时后': lambda m: int(m.group(1)) / 24,
            r'今天': 0,
        }
        
        # 时间格式模式
        self.time_formats = [
            r'(\d{1,2}):(\d{2})',  # 14:30
            r'(\d{1,2})点(\d{1,2})?分?',  # 2点30分
            r'上午(\d{1,2})点?',  # 上午9点
            r'下午(\d{1,2})点?',  # 下午2点
            r'晚上(\d{1,2})点?',  # 晚上8点
        ]
        
        # 优先级关键词
        self.priority_keywords = {
            '紧急': 3,
            '重要': 3,
            '急': 3,
            '马上': 3,
            '立即': 3,
            '普通': 2,
            '一般': 2,
            '不急': 1,
            '随时': 1,
        }
    
    def parse_task(self, user_input: str) -> Dict[str, Any]:
        """
        解析用户输入的任务
        返回: {
            'title': str,
            'description': str,
            'due_time': str,
            'priority': int
        }
        """
        try:
            # 提取时间信息
            due_time = self._extract_time_info(user_input)
            
            # 提取优先级
            priority = self._extract_priority(user_input)
            
            # 提取任务内容
            title, description = self._extract_task_content(user_input)
            
            return {
                'title': title,
                'description': description,
                'due_time': due_time,
                'priority': priority
            }
            
        except Exception as e:
            logger.error(f"任务解析失败: {e}")
            return {
                'title': user_input[:50],  # 截取前50个字符作为标题
                'description': user_input,
                'due_time': '',
                'priority': 2
            }
    
    def _extract_time_info(self, text: str) -> str:
        """提取时间信息"""
        now = datetime.now()
        
        # 检查相对时间
        for pattern, days in self.time_patterns.items():
            match = re.search(pattern, text)
            if match:
                if callable(days):
                    days = days(match)
                
                target_date = now + timedelta(days=days)
                
                # 检查具体时间
                time_str = self._extract_specific_time(text)
                if time_str:
                    try:
                        time_obj = datetime.strptime(time_str, '%H:%M').time()
                        target_datetime = datetime.combine(target_date.date(), time_obj)
                        return target_datetime.strftime('%Y-%m-%d %H:%M')
                    except:
                        pass
                
                return target_date.strftime('%Y-%m-%d')
        
        # 检查具体时间（今天）
        time_str = self._extract_specific_time(text)
        if time_str:
            try:
                time_obj = datetime.strptime(time_str, '%H:%M').time()
                target_datetime = datetime.combine(now.date(), time_obj)
                return target_datetime.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        return ''
    
    def _extract_specific_time(self, text: str) -> Optional[str]:
        """提取具体时间"""
        # 14:30 格式
        match = re.search(r'(\d{1,2}):(\d{2})', text)
        if match:
            hour, minute = match.groups()
            return f"{int(hour):02d}:{int(minute):02d}"
        
        # 2点30分 格式
        match = re.search(r'(\d{1,2})点(\d{1,2})?分?', text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            return f"{hour:02d}:{minute:02d}"
        
        # 上午/下午/晚上 格式
        for pattern, prefix in [
            (r'上午(\d{1,2})点?', 0),
            (r'下午(\d{1,2})点?', 12),
            (r'晚上(\d{1,2})点?', 18)
        ]:
            match = re.search(pattern, text)
            if match:
                hour = int(match.group(1))
                if prefix == 12 and hour != 12:  # 下午
                    hour += 12
                elif prefix == 18:  # 晚上
                    if hour < 6:
                        hour += 12
                return f"{hour:02d}:00"
        
        return None
    
    def _extract_priority(self, text: str) -> int:
        """提取优先级"""
        for keyword, priority in self.priority_keywords.items():
            if keyword in text:
                return priority
        return 2  # 默认普通优先级
    
    def _extract_task_content(self, text: str) -> Tuple[str, str]:
        """提取任务内容"""
        # 移除时间相关的词汇
        clean_text = text
        
        # 移除时间表达式
        time_remove_patterns = [
            r'明天|后天|大后天|今天|下周',
            r'\d+天后|\d+小时后',
            r'\d{1,2}:\d{2}',
            r'\d{1,2}点\d{1,2}?分?',
            r'上午\d{1,2}点?|下午\d{1,2}点?|晚上\d{1,2}点?',
        ]
        
        for pattern in time_remove_patterns:
            clean_text = re.sub(pattern, '', clean_text)
        
        # 移除优先级关键词
        for keyword in self.priority_keywords.keys():
            clean_text = clean_text.replace(keyword, '')
        
        # 清理多余空格
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # 如果文本太短，使用原文作为标题
        if len(clean_text) < 5:
            clean_text = text
        
        # 分割标题和描述
        if len(clean_text) > 30:
            title = clean_text[:30] + "..."
            description = clean_text
        else:
            title = clean_text
            description = text
        
        return title, description
    
    def generate_response(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """生成对话回复"""
        user_input_lower = user_input.lower()
        
        # 问候语
        if any(word in user_input_lower for word in ['你好', 'hi', 'hello', '哈基米']):
            return "你好！我是哈基米，你的桌面小助手！有什么可以帮你的吗？"
        
        # 任务相关
        if any(word in user_input_lower for word in ['任务', '提醒', '记住', '别忘了']):
            return "好的，我已经帮你记录了这个任务！到时候会提醒你的～"
        
        # 出行相关
        if any(word in user_input_lower for word in ['旅游', '出行', '去哪', '玩']):
            return "想出去玩呀？我可以帮你规划行程哦！告诉我目的地、预算和天数吧～"
        
        # 隐私相关
        if any(word in user_input_lower for word in ['隐私', '保护', '锁屏']):
            return "放心，我会帮你看好电脑的！离开时我会自动保护屏幕～"
        
        # 情感支持
        if any(word in user_input_lower for word in ['累', '疲惫', '压力', '烦']):
            return "辛苦了！要不要休息一下？我陪你聊聊天吧～"
        
        # 夸奖
        if any(word in user_input_lower for word in ['棒', '厉害', '好', '谢谢']):
            return "嘿嘿，谢谢夸奖！能帮到你我很开心～"
        
        # 默认回复
        responses = [
            "我在听呢！有什么需要帮助的吗？",
            "说得对！还有其他想聊的吗？",
            "嗯嗯，我明白了～",
            "有趣！继续说说看～",
            "我会记住的！还有什么要告诉我的吗？"
        ]
        
        import random
        return random.choice(responses)