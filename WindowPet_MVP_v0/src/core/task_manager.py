#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事务管理模块
负责任务的创建、管理和提醒
"""

import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable, Optional
import logging

from ai.nlp_processor import NLPProcessor
from utils.database import DatabaseManager

logger = logging.getLogger(__name__)

class TaskManager:
    """事务管理器"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.nlp_processor = NLPProcessor()
        self.reminder_thread = None
        self.is_running = False
        self.reminder_callback: Optional[Callable] = None
        
    def start_reminder_service(self, reminder_callback: Callable = None):
        """启动提醒服务"""
        if self.is_running:
            return
            
        self.reminder_callback = reminder_callback
        self.is_running = True
        self.reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()
        logger.info("任务提醒服务已启动")
    
    def stop_reminder_service(self):
        """停止提醒服务"""
        self.is_running = False
        if self.reminder_thread:
            self.reminder_thread.join(timeout=2)
        logger.info("任务提醒服务已停止")
    
    def add_task_from_text(self, user_input: str) -> Dict[str, Any]:
        """从用户输入文本添加任务"""
        try:
            # 使用NLP解析任务
            task_info = self.nlp_processor.parse_task(user_input)
            
            # 添加到数据库
            task_id = self.db_manager.add_task(
                title=task_info['title'],
                description=task_info['description'],
                due_time=task_info['due_time'],
                priority=task_info['priority']
            )
            
            task_info['id'] = task_id
            logger.info(f"添加任务成功: {task_info['title']}")
            return task_info
            
        except Exception as e:
            logger.error(f"添加任务失败: {e}")
            raise
    
    def get_tasks(self, status: str = None) -> List[Dict[str, Any]]:
        """获取任务列表"""
        return self.db_manager.get_tasks(status)
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """获取待办任务"""
        return self.get_tasks('pending')
    
    def complete_task(self, task_id: int):
        """完成任务"""
        self.db_manager.update_task_status(task_id, 'completed')
        logger.info(f"任务 {task_id} 已完成")
    
    def delete_task(self, task_id: int):
        """删除任务"""
        self.db_manager.delete_task(task_id)
        logger.info(f"任务 {task_id} 已删除")
    
    def get_upcoming_tasks(self, hours: int = 24) -> List[Dict[str, Any]]:
        """获取即将到期的任务"""
        tasks = self.get_pending_tasks()
        upcoming = []
        
        now = datetime.now()
        cutoff_time = now + timedelta(hours=hours)
        
        for task in tasks:
            if task['due_time']:
                try:
                    due_time = datetime.strptime(task['due_time'], '%Y-%m-%d %H:%M')
                    if now <= due_time <= cutoff_time:
                        upcoming.append(task)
                except ValueError:
                    # 只有日期，没有时间
                    try:
                        due_date = datetime.strptime(task['due_time'], '%Y-%m-%d')
                        if now.date() <= due_date.date() <= cutoff_time.date():
                            upcoming.append(task)
                    except ValueError:
                        continue
        
        return sorted(upcoming, key=lambda x: x['due_time'])
    
    def _reminder_loop(self):
        """提醒循环"""
        while self.is_running:
            try:
                self._check_reminders()
                time.sleep(60)  # 每分钟检查一次
            except Exception as e:
                logger.error(f"提醒检查出错: {e}")
                time.sleep(60)
    
    def _check_reminders(self):
        """检查需要提醒的任务"""
        now = datetime.now()
        tasks = self.get_pending_tasks()
        
        for task in tasks:
            if not task['due_time']:
                continue
                
            try:
                # 解析到期时间
                due_time = None
                if len(task['due_time']) > 10:  # 包含时间
                    due_time = datetime.strptime(task['due_time'], '%Y-%m-%d %H:%M')
                else:  # 只有日期
                    due_date = datetime.strptime(task['due_time'], '%Y-%m-%d')
                    due_time = due_date.replace(hour=9, minute=0)  # 默认上午9点提醒
                
                # 检查是否需要提醒（提前5分钟）
                reminder_time = due_time - timedelta(minutes=5)
                
                if now >= reminder_time and now < due_time:
                    # 检查是否已经提醒过（避免重复提醒）
                    last_reminder_key = f"last_reminder_{task['id']}"
                    last_reminder = self.db_manager.get_setting(last_reminder_key)
                    
                    if not last_reminder or last_reminder != task['due_time']:
                        # 触发提醒
                        if self.reminder_callback:
                            self.reminder_callback(task)
                        
                        # 记录提醒时间
                        self.db_manager.set_setting(last_reminder_key, task['due_time'])
                        logger.info(f"提醒任务: {task['title']}")
                
            except ValueError as e:
                logger.error(f"解析任务时间失败: {task['due_time']}, {e}")
                continue
    
    def get_task_statistics(self) -> Dict[str, int]:
        """获取任务统计信息"""
        all_tasks = self.get_tasks()
        
        stats = {
            'total': len(all_tasks),
            'pending': len([t for t in all_tasks if t['status'] == 'pending']),
            'completed': len([t for t in all_tasks if t['status'] == 'completed']),
            'overdue': 0
        }
        
        # 计算过期任务
        now = datetime.now()
        for task in all_tasks:
            if task['status'] == 'pending' and task['due_time']:
                try:
                    if len(task['due_time']) > 10:
                        due_time = datetime.strptime(task['due_time'], '%Y-%m-%d %H:%M')
                    else:
                        due_time = datetime.strptime(task['due_time'], '%Y-%m-%d')
                    
                    if now > due_time:
                        stats['overdue'] += 1
                except ValueError:
                    continue
        
        return stats