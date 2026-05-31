#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隐私保护模块
负责自动锁屏和隐私保护
"""

import os
import sys
import subprocess
import threading
import time
from typing import Callable, Optional
import logging

from ai.vision_detector import VisionDetector

logger = logging.getLogger(__name__)

class PrivacyGuard:
    """隐私保护器"""
    
    def __init__(self, detection_interval: float = 2.0, away_threshold: float = 30.0):
        self.detection_interval = detection_interval
        self.away_threshold = away_threshold
        self.vision_detector = None  # 延迟初始化，不在启动时创建
        self.is_active = False
        self.privacy_mode_active = False
        self.on_privacy_activated_callback: Optional[Callable] = None
        self.on_privacy_deactivated_callback: Optional[Callable] = None
        
    def start_protection(self, on_privacy_activated: Callable = None, 
                        on_privacy_deactivated: Callable = None):
        """启动隐私保护"""
        if self.is_active:
            return
            
        self.on_privacy_activated_callback = on_privacy_activated
        self.on_privacy_deactivated_callback = on_privacy_deactivated
        
        try:
            # 只有在需要时才初始化视觉检测器
            if self.vision_detector is None:
                self.vision_detector = VisionDetector(self.detection_interval, self.away_threshold)
            
            # 启动视觉检测
            self.vision_detector.start_monitoring(
                on_user_away=self._on_user_away,
                on_user_return=self._on_user_return
            )
            
            self.is_active = True
            logger.info("隐私保护已启动")
            
        except Exception as e:
            logger.error(f"启动隐私保护失败: {e}")
            # 即使摄像头不可用，也允许手动隐私模式
            self.is_active = True
    
    def stop_protection(self):
        """停止隐私保护"""
        if not self.is_active:
            return
            
        if self.vision_detector:
            self.vision_detector.stop_monitoring()
        
        self.is_active = False
        
        # 如果当前处于隐私模式，退出
        if self.privacy_mode_active:
            self._deactivate_privacy_mode()
        
        logger.info("隐私保护已停止")
    
    def _on_user_away(self):
        """用户离开时的处理"""
        if not self.privacy_mode_active:
            self._activate_privacy_mode()
    
    def _on_user_return(self):
        """用户返回时的处理"""
        if self.privacy_mode_active:
            self._deactivate_privacy_mode()
    
    def _activate_privacy_mode(self):
        """激活隐私模式"""
        try:
            # 锁定屏幕
            self._lock_screen()
            
            self.privacy_mode_active = True
            
            # 触发回调
            if self.on_privacy_activated_callback:
                self.on_privacy_activated_callback()
            
            logger.info("隐私模式已激活")
            
        except Exception as e:
            logger.error(f"激活隐私模式失败: {e}")
    
    def _deactivate_privacy_mode(self):
        """取消隐私模式"""
        try:
            self.privacy_mode_active = False
            
            # 触发回调
            if self.on_privacy_deactivated_callback:
                self.on_privacy_deactivated_callback()
            
            logger.info("隐私模式已取消")
            
        except Exception as e:
            logger.error(f"取消隐私模式失败: {e}")
    
    def _lock_screen(self):
        """锁定屏幕"""
        try:
            if sys.platform == "win32":
                # Windows系统锁屏
                import ctypes
                ctypes.windll.user32.LockWorkStation()
            elif sys.platform == "darwin":
                # macOS系统锁屏
                subprocess.run(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
            else:
                # Linux系统锁屏
                subprocess.run(["xdg-screensaver", "lock"])
                
            logger.info("屏幕已锁定")
            
        except Exception as e:
            logger.error(f"锁屏失败: {e}")
    
    def is_privacy_mode_active(self) -> bool:
        """检查隐私模式是否激活"""
        return self.privacy_mode_active
    
    def is_user_present(self) -> bool:
        """检查用户是否在场"""
        if self.vision_detector:
            return self.vision_detector.is_user_present()
        return True  # 如果没有视觉检测器，默认用户在场
    
    def force_activate_privacy(self):
        """手动激活隐私模式"""
        if not self.privacy_mode_active:
            self._activate_privacy_mode()
    
    def force_deactivate_privacy(self):
        """手动取消隐私模式"""
        if self.privacy_mode_active:
            self._deactivate_privacy_mode()
    
    def get_status(self) -> dict:
        """获取隐私保护状态"""
        return {
            'protection_active': self.is_active,
            'privacy_mode_active': self.privacy_mode_active,
            'user_present': self.is_user_present()
        }