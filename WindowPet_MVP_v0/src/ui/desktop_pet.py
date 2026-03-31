#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哈基米桌面宠物主界面
"""

import sys
import os
import random
import threading
import time
from pathlib import Path
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
        print("请安装 PyQt5 或 PySide2: pip install PyQt5")
        sys.exit(1)

from core.task_manager import TaskManager
from core.privacy_guard import PrivacyGuard
from core.travel_planner import TravelPlanner
from ai.nlp_processor import NLPProcessor
from utils.database import DatabaseManager
from utils.config import ConfigManager
from ui.dialogs_fixed import ChatDialog, TaskDialog, TravelDialog
import logging

logger = logging.getLogger(__name__)

class HakimiDesktopPet(QApplication):
    """哈基米桌面宠物主应用"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(sys.argv)
        
        self.config = config
        self.config_manager = ConfigManager()
        
        # 初始化数据库
        db_path = self.config_manager.get_data_path(config["database"]["path"])
        self.db_manager = DatabaseManager(str(db_path))
        
        # 初始化核心模块
        self.task_manager = TaskManager(self.db_manager)
        self.privacy_guard = PrivacyGuard(
            detection_interval=config["privacy"]["detection_interval"],
            away_threshold=config["privacy"]["away_threshold"]
        )
        self.travel_planner = TravelPlanner(self.db_manager)
        self.nlp_processor = NLPProcessor()
        
        # 初始化UI
        self.main_window = None
        self.chat_dialog = None
        self.task_dialog = None
        self.travel_dialog = None
        self.system_tray = None
        
        # 宠物状态
        self.current_image_index = 0
        self.animation_timer = None
        self.is_dragging = False
        
        self.init_ui()
        self.init_services()
    
    def init_ui(self):
        """初始化用户界面"""
        # 创建主窗口
        self.main_window = PetMainWindow(self)
        
        # 创建系统托盘
        self.init_system_tray()
        
        # 显示主窗口
        self.main_window.show()
        
        logger.info("UI初始化完成")
    
    def init_system_tray(self):
        """初始化系统托盘"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            logger.warning("系统托盘不可用")
            return
        
        self.system_tray = QSystemTrayIcon(self)
        
        # 设置托盘图标
        icon_path = self.config_manager.get_resource_path("pic1.jpg")
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path)).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.system_tray.setIcon(QIcon(pixmap))
        else:
            self.system_tray.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 显示/隐藏
        show_action = tray_menu.addAction("显示哈基米")
        show_action.triggered.connect(self.show_pet)
        
        hide_action = tray_menu.addAction("隐藏哈基米")
        hide_action.triggered.connect(self.hide_pet)
        
        tray_menu.addSeparator()
        
        # 功能菜单
        chat_action = tray_menu.addAction("💬 聊天")
        chat_action.triggered.connect(self.show_chat_dialog)
        
        task_action = tray_menu.addAction("📝 任务管理")
        task_action.triggered.connect(self.show_task_dialog)
        
        travel_action = tray_menu.addAction("✈️ 出行规划")
        travel_action.triggered.connect(self.show_travel_dialog)
        
        tray_menu.addSeparator()
        
        # 设置和退出
        settings_action = tray_menu.addAction("⚙️ 设置")
        settings_action.triggered.connect(self.show_settings)
        
        quit_action = tray_menu.addAction("❌ 退出")
        quit_action.triggered.connect(self.quit_application)
        
        self.system_tray.setContextMenu(tray_menu)
        self.system_tray.show()
        
        # 托盘消息
        self.system_tray.showMessage(
            "哈基米桌面宠物",
            "我已经准备好为你服务啦！",
            QSystemTrayIcon.Information,
            3000
        )
    
    def init_services(self):
        """初始化后台服务"""
        # 启动任务提醒服务
        self.task_manager.start_reminder_service(self.on_task_reminder)
        
        # 隐私保护默认不启动，只有用户手动开启时才启动
        # if self.config["features"]["privacy_guard"]:
        #     self.privacy_guard.start_protection(
        #         on_privacy_activated=self.on_privacy_activated,
        #         on_privacy_deactivated=self.on_privacy_deactivated
        #     )
        
        logger.info("后台服务启动完成")
    
    def show_pet(self):
        """显示宠物"""
        if self.main_window:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
    
    def hide_pet(self):
        """隐藏宠物"""
        if self.main_window:
            self.main_window.hide()
    
    def show_chat_dialog(self):
        """显示聊天对话框"""
        if not self.chat_dialog:
            self.chat_dialog = ChatDialog(self)
        self.chat_dialog.show()
        self.chat_dialog.raise_()
        self.chat_dialog.activateWindow()
    
    def show_task_dialog(self):
        """显示任务管理对话框"""
        if not self.task_dialog:
            self.task_dialog = TaskDialog(self)
        self.task_dialog.show()
        self.task_dialog.raise_()
        self.task_dialog.activateWindow()
    
    def show_travel_dialog(self):
        """显示出行规划对话框"""
        if not self.travel_dialog:
            self.travel_dialog = TravelDialog(self)
        self.travel_dialog.show()
        self.travel_dialog.raise_()
        self.travel_dialog.activateWindow()
    
    def show_settings(self):
        """显示设置对话框"""
        QMessageBox.information(None, "设置", "设置功能开发中...")
    
    def quit_application(self):
        """退出应用"""
        # 停止服务
        self.task_manager.stop_reminder_service()
        self.privacy_guard.stop_protection()
        
        # 退出应用
        self.quit()
    
    def on_task_reminder(self, task: Dict[str, Any]):
        """任务提醒回调"""
        if self.system_tray:
            self.system_tray.showMessage(
                "任务提醒",
                f"⏰ {task['title']}\n{task.get('description', '')}",
                QSystemTrayIcon.Information,
                5000
            )
        
        # 显示宠物并播放提醒动画
        self.show_pet()
        if self.main_window:
            self.main_window.play_reminder_animation()
    
    def on_privacy_activated(self):
        """隐私模式激活回调"""
        logger.info("隐私保护已激活")
        if self.main_window:
            self.main_window.set_privacy_mode(True)
    
    def on_privacy_deactivated(self):
        """隐私模式取消回调"""
        logger.info("隐私保护已取消")
        if self.main_window:
            self.main_window.set_privacy_mode(False)
    
    def run(self) -> int:
        """运行应用"""
        return self.exec_()


class PetMainWindow(QWidget):
    """宠物主窗口"""
    
    def __init__(self, app: HakimiDesktopPet):
        super().__init__()
        self.app = app
        self.config = app.config
        self.config_manager = app.config_manager
        
        # 窗口状态
        self.is_privacy_mode = False
        self.drag_position = QPoint()
        
        # 加载宠物图片
        self.pet_images = self.load_pet_images()
        self.current_image_index = 0
        
        # 动画定时器
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.next_animation_frame)
        
        self.init_window()
        self.start_idle_animation()
    
    def init_window(self):
        """初始化窗口"""
        # 窗口设置
        self.setWindowTitle(self.config["app"]["name"])
        self.setFixedSize(
            self.config["ui"]["window_size"]["width"],
            self.config["ui"]["window_size"]["height"]
        )
        
        # 窗口标志
        flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        self.setWindowFlags(flags)
        
        # 透明背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 初始位置（屏幕右下角）
        screen = QApplication.desktop().screenGeometry()
        self.move(screen.width() - self.width() - 50, screen.height() - self.height() - 100)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 宠物图片标签
        self.pet_label = QLabel()
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setScaledContents(True)
        
        # 设置初始图片
        if self.pet_images:
            self.pet_label.setPixmap(self.pet_images[0])
        
        layout.addWidget(self.pet_label)
        
        self.setLayout(layout)
        
        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def load_pet_images(self) -> List[QPixmap]:
        """加载宠物图片"""
        images = []
        
        for img_name in self.config["pet"]["images"]:
            img_path = self.config_manager.get_resource_path(img_name)
            if img_path.exists():
                pixmap = QPixmap(str(img_path))
                # 缩放图片
                scaled_pixmap = pixmap.scaled(
                    self.config["ui"]["window_size"]["width"],
                    self.config["ui"]["window_size"]["height"],
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                images.append(scaled_pixmap)
        
        # 如果没有找到图片，创建默认图片
        if not images:
            default_pixmap = QPixmap(150, 150)
            default_pixmap.fill(Qt.transparent)
            
            painter = QPainter(default_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 绘制简单的哈基米形象
            painter.setBrush(QBrush(QColor(255, 200, 100)))  # 橙色
            painter.drawEllipse(25, 25, 100, 100)
            
            # 眼睛
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawEllipse(45, 55, 15, 15)
            painter.drawEllipse(90, 55, 15, 15)
            
            # 嘴巴
            painter.setPen(QPen(QColor(0, 0, 0), 3))
            painter.drawArc(55, 75, 40, 30, 0, 180 * 16)
            
            painter.end()
            images.append(default_pixmap)
        
        return images
    
    def start_idle_animation(self):
        """开始待机动画"""
        if self.config["pet"]["idle_animations"]:
            self.animation_timer.start(self.config["pet"]["animation_speed"])
    
    def stop_idle_animation(self):
        """停止待机动画"""
        self.animation_timer.stop()
    
    def next_animation_frame(self):
        """下一帧动画"""
        if self.pet_images and not self.is_privacy_mode:
            self.current_image_index = (self.current_image_index + 1) % len(self.pet_images)
            self.pet_label.setPixmap(self.pet_images[self.current_image_index])
    
    def play_reminder_animation(self):
        """播放提醒动画"""
        # 简单的闪烁效果
        for _ in range(3):
            QTimer.singleShot(200, lambda: self.setWindowOpacity(0.3))
            QTimer.singleShot(400, lambda: self.setWindowOpacity(1.0))
    
    def set_privacy_mode(self, enabled: bool):
        """设置隐私模式"""
        self.is_privacy_mode = enabled
        
        if enabled:
            # 隐私模式：显示保护图标
            self.stop_idle_animation()
            
            # 创建保护图标
            privacy_pixmap = QPixmap(150, 150)
            privacy_pixmap.fill(Qt.transparent)
            
            painter = QPainter(privacy_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # 绘制盾牌图标
            painter.setBrush(QBrush(QColor(255, 0, 0, 150)))
            painter.drawEllipse(25, 25, 100, 100)
            
            painter.setPen(QPen(QColor(255, 255, 255), 5))
            painter.drawText(50, 85, "🔒")
            
            painter.end()
            
            self.pet_label.setPixmap(privacy_pixmap)
        else:
            # 恢复正常模式
            if self.pet_images:
                self.pet_label.setPixmap(self.pet_images[self.current_image_index])
            self.start_idle_animation()
    
    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)
        
        # 聊天
        chat_action = menu.addAction("💬 和哈基米聊天")
        chat_action.triggered.connect(self.app.show_chat_dialog)
        
        # 任务管理
        task_action = menu.addAction("📝 任务管理")
        task_action.triggered.connect(self.app.show_task_dialog)
        
        # 出行规划
        travel_action = menu.addAction("✈️ 出行规划")
        travel_action.triggered.connect(self.app.show_travel_dialog)
        
        menu.addSeparator()
        
        # 隐私保护
        privacy_action = menu.addAction("🔒 隐私保护")
        privacy_action.setCheckable(True)
        privacy_action.setChecked(self.app.privacy_guard.is_privacy_mode_active())
        privacy_action.triggered.connect(self.toggle_privacy_protection)
        
        menu.addSeparator()
        
        # 隐藏
        hide_action = menu.addAction("👻 隐藏")
        hide_action.triggered.connect(self.hide)
        
        # 退出
        quit_action = menu.addAction("❌ 退出")
        quit_action.triggered.connect(self.app.quit_application)
        
        menu.exec_(self.mapToGlobal(position))
    
    def toggle_privacy_protection(self):
        """切换隐私保护"""
        if self.app.privacy_guard.is_privacy_mode_active():
            self.app.privacy_guard.force_deactivate_privacy()
        else:
            # 只有在用户手动开启时才启动隐私保护服务
            if not self.app.privacy_guard.is_active:
                self.app.privacy_guard.start_protection(
                    on_privacy_activated=self.app.on_privacy_activated,
                    on_privacy_deactivated=self.app.on_privacy_deactivated
                )
            self.app.privacy_guard.force_activate_privacy()
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件（拖拽）"""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            # 双击打开聊天对话框
            self.app.show_chat_dialog()
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        # 鼠标悬停时稍微放大
        self.setWindowOpacity(0.9)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        # 恢复正常透明度
        self.setWindowOpacity(1.0)