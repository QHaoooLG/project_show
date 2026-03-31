#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈基米桌面宠物 MVP - 主程序入口
基于"全链路自我验证"的桌面智能助手

核心功能：
1. 智能事务管理 - 30秒内完成任务记录
2. 自动隐私保护 - 离开时自动保护屏幕  
3. 快速出行规划 - 10分钟内生成出行方案
4. 桌面陪伴交互 - 提供情感价值和操作反馈
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from ui.desktop_pet import HakimiDesktopPet
from utils.logger import setup_logger
from utils.config import ConfigManager

def main():
    """主程序入口"""
    try:
        # 设置日志
        logger = setup_logger()
        logger.info("=== 哈基米桌面宠物 MVP 启动 ===")
        
        # 加载配置
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # 创建并启动桌面宠物
        app = HakimiDesktopPet(config)
        
        logger.info("桌面宠物启动成功")
        return app.run()
        
    except Exception as e:
        logging.error(f"程序启动失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())