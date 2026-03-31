#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理模块
负责SQLite数据库的创建和管理
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 任务表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_time TEXT,
                    priority INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 聊天记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 出行计划表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS travel_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    budget REAL,
                    days INTEGER,
                    preferences TEXT,
                    plan_data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 用户设置表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def add_task(self, title: str, description: str = "", due_time: str = "", priority: int = 1) -> int:
        """添加任务"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (title, description, due_time, priority)
                VALUES (?, ?, ?, ?)
            ''', (title, description, due_time, priority))
            conn.commit()
            return cursor.lastrowid
    
    def get_tasks(self, status: str = None) -> List[Dict[str, Any]]:
        """获取任务列表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status,))
            else:
                cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def update_task_status(self, task_id: int, status: str):
        """更新任务状态"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks SET status = ?, updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (status, task_id))
            conn.commit()
    
    def delete_task(self, task_id: int):
        """删除任务"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
    
    def add_chat_record(self, user_message: str, bot_response: str):
        """添加聊天记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chat_history (user_message, bot_response)
                VALUES (?, ?)
            ''', (user_message, bot_response))
            conn.commit()
    
    def get_chat_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取聊天历史"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM chat_history 
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def save_travel_plan(self, title: str, destination: str, budget: float, 
                        days: int, preferences: str, plan_data: Dict[str, Any]) -> int:
        """保存出行计划"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO travel_plans (title, destination, budget, days, preferences, plan_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, destination, budget, days, preferences, json.dumps(plan_data, ensure_ascii=False)))
            conn.commit()
            return cursor.lastrowid
    
    def get_travel_plans(self) -> List[Dict[str, Any]]:
        """获取出行计划列表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM travel_plans ORDER BY created_at DESC')
            
            columns = [description[0] for description in cursor.description]
            plans = []
            for row in cursor.fetchall():
                plan = dict(zip(columns, row))
                if plan['plan_data']:
                    plan['plan_data'] = json.loads(plan['plan_data'])
                plans.append(plan)
            return plans
    
    def set_setting(self, key: str, value: str):
        """设置用户配置"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
            conn.commit()
    
    def get_setting(self, key: str, default: str = None) -> Optional[str]:
        """获取用户配置"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM user_settings WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result[0] if result else default