#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版对话框模块 - 用于测试
"""

import sys
from datetime import datetime
from typing import Dict, Any, List

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    try:
        from PySide2.QtWidgets import *
        from PySide2.QtCore import *
        from PySide2.QtGui import *
    except ImportError:
        print("请安装 PyQt5 或 PySide2")
        sys.exit(1)

print("Defining ChatDialog...")

class ChatDialog(QDialog):
    """聊天对话框"""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("💬 和哈基米聊天")
        self.setFixedSize(400, 500)

print("ChatDialog defined successfully")

class TaskDialog(QDialog):
    """任务管理对话框"""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("📝 任务管理")
        self.setFixedSize(600, 500)

print("TaskDialog defined successfully")

class TravelDialog(QDialog):
    """出行规划对话框"""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("✈️ 出行规划")
        self.setFixedSize(700, 600)

print("TravelDialog defined successfully")
print("All dialogs defined successfully!")