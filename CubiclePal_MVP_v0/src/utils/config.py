#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责加载和管理应用配置
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
        self.resource_dir = self.project_root / "resource"
        self.data_dir = self.project_root / "data"
        
        # 确保数据目录存在
        self.data_dir.mkdir(exist_ok=True)
        
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_path = self.resource_dir / "config.yaml"
        
        # 默认配置
        default_config = {
            "app": {
                "name": "哈基米桌面宠物",
                "version": "1.0.0",
                "debug": True
            },
            "ui": {
                "window_size": {"width": 150, "height": 150},
                "transparency": 0.9,
                "always_on_top": True,
                "frameless": True
            },
            "pet": {
                "name": "哈基米",
                "images": ["pic1.jpg", "pic2.jpg", "pic3.jpg", "pic4.jpg"],
                "animation_speed": 2000,  # 毫秒
                "idle_animations": True
            },
            "features": {
                "task_manager": True,
                "privacy_guard": True,
                "travel_planner": True,
                "chat": True
            },
            "ai": {
                "provider": "local",  # local/deepseek
                "api_key": "",
                "timeout": 10
            },
            "privacy": {
                "face_detection": True,
                "detection_interval": 2.0,
                "away_threshold": 30
            },
            "database": {
                "path": "data/hakimi.db"
            }
        }
        
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
                    # 合并配置
                    default_config.update(file_config)
        except Exception as e:
            print(f"配置文件加载失败，使用默认配置: {e}")
            
        return default_config
    
    def get_resource_path(self, filename: str) -> Path:
        """获取资源文件路径"""
        return self.resource_dir / filename
    
    def get_data_path(self, filename: str) -> Path:
        """获取数据文件路径"""
        return self.data_dir / filename