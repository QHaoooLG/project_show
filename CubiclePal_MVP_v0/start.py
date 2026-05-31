#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈基米桌面宠物启动脚本
简化版启动器，用于快速测试
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def check_dependencies():
    """检查依赖"""
    missing_deps = []
    
    try:
        import yaml
    except ImportError:
        missing_deps.append("PyYAML")
    
    try:
        from PyQt5.QtWidgets import QApplication
    except ImportError:
        try:
            from PySide2.QtWidgets import QApplication
        except ImportError:
            missing_deps.append("PyQt5 或 PySide2")
    
    if missing_deps:
        print("❌ 缺少依赖包:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n请运行: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """主函数"""
    print("🎯 哈基米桌面宠物 MVP 启动中...")
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    try:
        # 导入并启动应用
        from ui.desktop_pet import HakimiDesktopPet
        from utils.config import ConfigManager
        from utils.logger import setup_logger
        
        # 设置日志
        logger = setup_logger()
        logger.info("哈基米桌面宠物启动")
        
        # 加载配置
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        print("✅ 配置加载完成")
        print(f"📱 宠物名称: {config['pet']['name']}")
        print("🚀 启动桌面宠物...")
        
        # 创建并运行应用
        app = HakimiDesktopPet(config)
        return app.run()
        
    except KeyboardInterrupt:
        print("\n👋 用户取消启动")
        return 0
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())