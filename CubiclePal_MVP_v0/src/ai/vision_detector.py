#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算机视觉模块
负责人脸检测和隐私保护
"""

import cv2
import numpy as np
import threading
import time
from typing import Callable, Optional
import logging

logger = logging.getLogger(__name__)

class VisionDetector:
    """视觉检测器"""
    
    def __init__(self, detection_interval: float = 2.0, away_threshold: float = 30.0):
        self.detection_interval = detection_interval
        self.away_threshold = away_threshold
        self.is_running = False
        self.last_detection_time = time.time()
        self.face_cascade = None
        self.camera = None
        self.detection_thread = None
        self.on_user_away_callback: Optional[Callable] = None
        self.on_user_return_callback: Optional[Callable] = None
        self.user_present = True
        
        # 初始化人脸检测器
        self._init_face_detector()
    
    def _init_face_detector(self):
        """初始化人脸检测器"""
        try:
            # 尝试加载OpenCV的人脸检测器
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            logger.info("人脸检测器初始化成功")
        except Exception as e:
            logger.error(f"人脸检测器初始化失败: {e}")
            self.face_cascade = None
    
    def start_monitoring(self, on_user_away: Callable = None, on_user_return: Callable = None):
        """开始监控用户状态"""
        if self.is_running:
            return
        
        self.on_user_away_callback = on_user_away
        self.on_user_return_callback = on_user_return
        
        try:
            # 初始化摄像头
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                logger.warning("无法打开摄像头，隐私保护功能将不可用")
                return
            
            self.is_running = True
            self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
            self.detection_thread.start()
            logger.info("用户状态监控已启动")
            
        except Exception as e:
            logger.error(f"启动用户监控失败: {e}")
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        if self.detection_thread:
            self.detection_thread.join(timeout=2)
        
        logger.info("用户状态监控已停止")
    
    def _detection_loop(self):
        """检测循环"""
        while self.is_running:
            try:
                faces_detected = self._detect_faces()
                current_time = time.time()
                
                if faces_detected:
                    self.last_detection_time = current_time
                    if not self.user_present:
                        # 用户返回
                        self.user_present = True
                        if self.on_user_return_callback:
                            self.on_user_return_callback()
                        logger.info("检测到用户返回")
                else:
                    # 检查用户是否离开太久
                    time_away = current_time - self.last_detection_time
                    if time_away > self.away_threshold and self.user_present:
                        # 用户离开
                        self.user_present = False
                        if self.on_user_away_callback:
                            self.on_user_away_callback()
                        logger.info(f"检测到用户离开 ({time_away:.1f}秒)")
                
                time.sleep(self.detection_interval)
                
            except Exception as e:
                logger.error(f"人脸检测出错: {e}")
                time.sleep(self.detection_interval)
    
    def _detect_faces(self) -> bool:
        """检测人脸"""
        if not self.camera or not self.face_cascade:
            return True  # 如果检测器不可用，假设用户在场
        
        try:
            ret, frame = self.camera.read()
            if not ret:
                return True
            
            # 转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 检测人脸
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            return len(faces) > 0
            
        except Exception as e:
            logger.error(f"人脸检测处理失败: {e}")
            return True
    
    def is_user_present(self) -> bool:
        """检查用户是否在场"""
        return self.user_present
    
    def force_check(self) -> bool:
        """强制检查一次用户状态"""
        if not self.is_running:
            return True
        return self._detect_faces()