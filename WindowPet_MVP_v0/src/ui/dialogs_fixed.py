#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版对话框模块
包含聊天、任务管理、出行规划等对话框
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

import logging
logger = logging.getLogger(__name__)


class ChatDialog(QDialog):
    """聊天对话框"""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setAttribute(Qt.WA_DeleteOnClose, False)  # 防止关闭时删除对象
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.init_ui()
        self.load_chat_history()
    
    def closeEvent(self, event):
        """重写关闭事件，隐藏而不是关闭"""
        self.hide()
        event.ignore()  # 忽略关闭事件，防止窗口被销毁
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("💬 和哈基米聊天")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        layout = QVBoxLayout()
        
        # 聊天记录区域
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.chat_area)
        
        # 输入区域
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入消息...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_button = QPushButton("发送")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # 快捷按钮
        shortcuts_layout = QHBoxLayout()
        
        task_btn = QPushButton("📝 添加任务")
        task_btn.clicked.connect(lambda: self.quick_input("帮我添加一个任务："))
        
        travel_btn = QPushButton("✈️ 规划出行")
        travel_btn.clicked.connect(lambda: self.quick_input("我想去旅游："))
        
        shortcuts_layout.addWidget(task_btn)
        shortcuts_layout.addWidget(travel_btn)
        
        layout.addLayout(shortcuts_layout)
        
        self.setLayout(layout)
        
        # 欢迎消息
        self.add_message("哈基米", "你好！我是哈基米，你的桌面小助手！有什么可以帮你的吗？", True)
    
    def load_chat_history(self):
        """加载聊天历史"""
        try:
            if hasattr(self.app, 'db_manager'):
                history = self.app.db_manager.get_chat_history(20)
                for record in reversed(history):  # 按时间顺序显示
                    self.add_message("你", record["user_message"], False)
                    self.add_message("哈基米", record["bot_response"], True)
        except Exception as e:
            logger.error(f"加载聊天历史失败: {e}")
    
    def quick_input(self, text: str):
        """快捷输入"""
        self.input_field.setText(text)
        self.input_field.setFocus()
    
    def send_message(self):
        """发送消息"""
        message = self.input_field.text().strip()
        if not message:
            return
        
        # 显示用户消息
        self.add_message("你", message, False)
        self.input_field.clear()
        
        # 处理消息
        self.process_message(message)
    
    def process_message(self, message: str):
        """处理用户消息"""
        try:
            # 检查是否是任务相关
            if any(word in message.lower() for word in ['任务', '提醒', '记住', '别忘了']):
                if hasattr(self.app, 'task_manager'):
                    task_info = self.app.task_manager.add_task_from_text(message)
                    response = f"好的！我已经帮你记录了任务：{task_info['title']}"
                    if task_info.get('due_time'):
                        response += f"\n⏰ 提醒时间：{task_info['due_time']}"
                else:
                    response = "任务管理功能暂时不可用，但我已经记住你的话了！"
            
            # 检查是否是出行相关
            elif any(word in message.lower() for word in ['旅游', '出行', '去哪', '玩']):
                if hasattr(self.app, 'travel_planner'):
                    travel_info = self.app.travel_planner.parse_travel_request(message)
                    if travel_info.get('destination'):
                        response = f"想去{travel_info['destination']}玩呀！我来帮你规划一下行程～"
                    else:
                        response = "想出去玩呀？告诉我目的地、预算和天数，我来帮你规划行程！"
                else:
                    response = "出行规划功能暂时不可用，但听起来很有趣！"
            
            else:
                # 普通对话
                if hasattr(self.app, 'nlp_processor'):
                    response = self.app.nlp_processor.generate_response(message)
                else:
                    # 简单的回复逻辑
                    responses = [
                        "我明白了！",
                        "这很有趣呢！",
                        "告诉我更多吧！",
                        "我在认真听着～",
                        "你说得对！"
                    ]
                    import random
                    response = random.choice(responses)
            
            # 显示回复
            self.add_message("哈基米", response, True)
            
            # 保存聊天记录
            if hasattr(self.app, 'db_manager'):
                self.app.db_manager.add_chat_record(message, response)
            
        except Exception as e:
            logger.error(f"处理消息失败: {e}")
            self.add_message("哈基米", "抱歉，我遇到了一些问题，请稍后再试～", True)
    
    def add_message(self, sender: str, message: str, is_bot: bool):
        """添加消息到聊天区域"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if is_bot:
            color = "#4CAF50"
            align = "left"
        else:
            color = "#2196F3"
            align = "right"
        
        html = f"""
        <div style="margin: 5px 0; text-align: {align};">
            <div style="display: inline-block; max-width: 70%; background-color: {color}; 
                        color: white; padding: 8px 12px; border-radius: 12px; 
                        font-size: 14px; line-height: 1.4;">
                <strong>{sender}</strong> <span style="font-size: 12px; opacity: 0.8;">{timestamp}</span><br>
                {message}
            </div>
        </div>
        """
        
        self.chat_area.append(html)
        
        # 滚动到底部
        scrollbar = self.chat_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


class TaskDialog(QDialog):
    """任务管理对话框"""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setAttribute(Qt.WA_DeleteOnClose, False)  # 防止关闭时删除对象
        self.init_ui()
        self.refresh_tasks()
    
    def closeEvent(self, event):
        """重写关闭事件，隐藏而不是关闭"""
        self.hide()
        event.ignore()  # 忽略关闭事件，防止窗口被销毁
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("📝 任务管理")
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout()
        
        # 顶部工具栏
        toolbar = QHBoxLayout()
        
        self.add_button = QPushButton("➕ 添加任务")
        self.add_button.clicked.connect(self.add_task)
        
        self.refresh_button = QPushButton("🔄 刷新")
        self.refresh_button.clicked.connect(self.refresh_tasks)
        
        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.refresh_button)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # 任务列表
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
        self.task_list.itemDoubleClicked.connect(self.edit_task)
        
        layout.addWidget(self.task_list)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        
        self.complete_button = QPushButton("✅ 完成")
        self.complete_button.clicked.connect(self.complete_task)
        
        self.delete_button = QPushButton("🗑️ 删除")
        self.delete_button.clicked.connect(self.delete_task)
        
        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def refresh_tasks(self):
        """刷新任务列表"""
        self.task_list.clear()
        
        try:
            if hasattr(self.app, 'task_manager'):
                tasks = self.app.task_manager.get_pending_tasks()
                
                for task in tasks:
                    item_widget = QWidget()
                    item_layout = QVBoxLayout()
                    
                    # 任务标题
                    title_label = QLabel(task['title'])
                    title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
                    
                    # 任务详情
                    details = []
                    if task.get('due_time'):
                        details.append(f"⏰ {task['due_time']}")
                    if task.get('priority') == 3:
                        details.append("🔴 高优先级")
                    elif task.get('priority') == 1:
                        details.append("🟢 低优先级")
                    
                    if details:
                        detail_label = QLabel(" | ".join(details))
                        detail_label.setStyleSheet("color: #666; font-size: 12px;")
                        item_layout.addWidget(detail_label)
                    
                    item_layout.addWidget(title_label)
                    
                    if task.get('description') and task['description'] != task['title']:
                        desc_label = QLabel(task['description'])
                        desc_label.setStyleSheet("color: #888; font-size: 12px;")
                        desc_label.setWordWrap(True)
                        item_layout.addWidget(desc_label)
                    
                    item_widget.setLayout(item_layout)
                    
                    list_item = QListWidgetItem()
                    list_item.setSizeHint(item_widget.sizeHint())
                    list_item.setData(Qt.UserRole, task)
                    
                    self.task_list.addItem(list_item)
                    self.task_list.setItemWidget(list_item, item_widget)
            else:
                # 显示示例任务
                example_item = QListWidgetItem("任务管理功能暂时不可用")
                self.task_list.addItem(example_item)
                
        except Exception as e:
            logger.error(f"刷新任务列表失败: {e}")
            error_item = QListWidgetItem(f"加载任务失败: {e}")
            self.task_list.addItem(error_item)
    
    def add_task(self):
        """添加任务"""
        dialog = AddTaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            task_data = dialog.get_task_data()
            try:
                if hasattr(self.app, 'task_manager'):
                    self.app.task_manager.add_task_from_text(task_data['text'])
                    self.refresh_tasks()
                    QMessageBox.information(self, "成功", "任务添加成功！")
                else:
                    QMessageBox.information(self, "提示", "任务管理功能暂时不可用")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"添加任务失败：{e}")
    
    def edit_task(self, item):
        """编辑任务"""
        task = item.data(Qt.UserRole)
        if task:
            QMessageBox.information(self, "任务详情", 
                                  f"标题：{task['title']}\n"
                                  f"描述：{task.get('description', '无')}\n"
                                  f"截止时间：{task.get('due_time', '无')}\n"
                                  f"状态：{task.get('status', '未知')}")
    
    def complete_task(self):
        """完成任务"""
        current_item = self.task_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请选择要完成的任务")
            return
        
        task = current_item.data(Qt.UserRole)
        if task and hasattr(self.app, 'task_manager'):
            try:
                self.app.task_manager.complete_task(task['id'])
                self.refresh_tasks()
                QMessageBox.information(self, "成功", "任务已完成！")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"完成任务失败：{e}")
    
    def delete_task(self):
        """删除任务"""
        current_item = self.task_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "提示", "请选择要删除的任务")
            return
        
        task = current_item.data(Qt.UserRole)
        if task:
            reply = QMessageBox.question(self, "确认", f"确定要删除任务「{task['title']}」吗？")
            
            if reply == QMessageBox.Yes:
                try:
                    if hasattr(self.app, 'task_manager'):
                        self.app.task_manager.delete_task(task['id'])
                        self.refresh_tasks()
                        QMessageBox.information(self, "成功", "任务已删除！")
                    else:
                        QMessageBox.information(self, "提示", "任务管理功能暂时不可用")
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"删除任务失败：{e}")


class AddTaskDialog(QDialog):
    """添加任务对话框"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("添加任务")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        # 任务输入
        layout.addWidget(QLabel("请描述你的任务："))
        
        self.task_input = QTextEdit()
        self.task_input.setPlaceholderText("例如：明天下午2点开会")
        self.task_input.setMaximumHeight(80)
        layout.addWidget(self.task_input)
        
        # 按钮
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_task_data(self):
        """获取任务数据"""
        return {
            'text': self.task_input.toPlainText().strip()
        }


class TravelDialog(QDialog):
    """出行规划对话框"""
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.current_plans = []
        self.setAttribute(Qt.WA_DeleteOnClose, False)  # 防止关闭时删除对象
        self.init_ui()
    
    def closeEvent(self, event):
        """重写关闭事件，隐藏而不是关闭"""
        self.hide()
        event.ignore()  # 忽略关闭事件，防止窗口被销毁
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✈️ 出行规划")
        self.setFixedSize(700, 600)
        
        layout = QVBoxLayout()
        
        # 输入区域
        input_group = QGroupBox("出行需求")
        input_layout = QFormLayout()
        
        self.destination_input = QLineEdit()
        self.destination_input.setPlaceholderText("如：北京、上海、杭州")
        
        self.budget_input = QSpinBox()
        self.budget_input.setRange(100, 50000)
        self.budget_input.setValue(1000)
        self.budget_input.setSuffix(" 元")
        
        self.days_input = QSpinBox()
        self.days_input.setRange(1, 30)
        self.days_input.setValue(2)
        self.days_input.setSuffix(" 天")
        
        self.preference_input = QLineEdit()
        self.preference_input.setPlaceholderText("如：美食、历史、自然风光")
        
        input_layout.addRow("目的地：", self.destination_input)
        input_layout.addRow("预算：", self.budget_input)
        input_layout.addRow("天数：", self.days_input)
        input_layout.addRow("偏好：", self.preference_input)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # 生成按钮
        self.generate_button = QPushButton("🎯 生成行程方案")
        self.generate_button.clicked.connect(self.generate_plans)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        layout.addWidget(self.generate_button)
        
        # 方案显示区域
        self.plans_area = QTabWidget()
        layout.addWidget(self.plans_area)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("💾 保存方案")
        self.save_button.clicked.connect(self.save_current_plan)
        self.save_button.setEnabled(False)
        
        self.export_button = QPushButton("📄 导出方案")
        self.export_button.clicked.connect(self.export_plan)
        self.export_button.setEnabled(False)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def generate_plans(self):
        """生成出行方案"""
        destination = self.destination_input.text().strip()
        if not destination:
            QMessageBox.warning(self, "提示", "请输入目的地")
            return
        
        budget = self.budget_input.value()
        days = self.days_input.value()
        preferences = self.preference_input.text().strip()
        
        # 显示加载状态
        self.generate_button.setText("🔄 生成中...")
        self.generate_button.setEnabled(False)
        
        try:
            if hasattr(self.app, 'travel_planner'):
                # 生成方案
                plans = self.app.travel_planner.generate_travel_plan(
                    destination, budget, days, preferences
                )
                
                self.current_plans = plans
                self.display_plans(plans)
                
                # 启用按钮
                self.save_button.setEnabled(True)
                self.export_button.setEnabled(True)
            else:
                # 显示示例方案
                example_plan = {
                    'title': f'{destination}{days}日游',
                    'destination': destination,
                    'days': days,
                    'budget': budget,
                    'estimated_cost': budget * 0.8,
                    'plan_type': '经济型'
                }
                self.current_plans = [example_plan]
                self.display_plans([example_plan])
                QMessageBox.information(self, "提示", "出行规划功能暂时不可用，显示示例方案")
            
        except Exception as e:
            logger.error(f"生成出行方案失败: {e}")
            QMessageBox.warning(self, "错误", f"生成方案失败：{e}")
        
        finally:
            self.generate_button.setText("🎯 生成行程方案")
            self.generate_button.setEnabled(True)
    
    def display_plans(self, plans: List[Dict[str, Any]]):
        """显示方案"""
        self.plans_area.clear()
        
        for i, plan in enumerate(plans):
            tab_widget = QWidget()
            tab_layout = QVBoxLayout()
            
            # 方案概览
            overview = QTextEdit()
            overview.setReadOnly(True)
            overview.setMaximumHeight(150)
            
            overview_text = f"""
            <h3>{plan['title']}</h3>
            <p><strong>目的地：</strong>{plan['destination']}</p>
            <p><strong>天数：</strong>{plan['days']}天</p>
            <p><strong>预算：</strong>{plan['budget']}元</p>
            <p><strong>预计费用：</strong>{plan.get('estimated_cost', 0):.0f}元</p>
            <p><strong>方案类型：</strong>{plan.get('plan_type', '标准型')}</p>
            """
            
            overview.setHtml(overview_text)
            tab_layout.addWidget(overview)
            
            # 详细行程
            schedule_area = QTextEdit()
            schedule_area.setReadOnly(True)
            
            schedule_html = "<h4>📅 详细行程</h4>"
            if 'daily_schedule' in plan:
                for day_info in plan['daily_schedule']:
                    schedule_html += f"<h5>第{day_info['day']}天</h5><ul>"
                    for attraction in day_info['attractions']:
                        schedule_html += f"<li>{attraction['name']} - {attraction['duration']}小时 - {attraction['cost']}元</li>"
                    schedule_html += "</ul>"
            else:
                schedule_html += "<p>详细行程正在规划中...</p>"
            
            schedule_area.setHtml(schedule_html)
            tab_layout.addWidget(schedule_area)
            
            tab_widget.setLayout(tab_layout)
            self.plans_area.addTab(tab_widget, f"方案{i+1}")
    
    def save_current_plan(self):
        """保存当前方案"""
        current_index = self.plans_area.currentIndex()
        if current_index >= 0 and current_index < len(self.current_plans):
            plan = self.current_plans[current_index]
            try:
                if hasattr(self.app, 'travel_planner'):
                    self.app.travel_planner.save_plan(plan)
                    QMessageBox.information(self, "成功", "方案保存成功！")
                else:
                    QMessageBox.information(self, "提示", "保存功能暂时不可用")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"保存失败：{e}")
    
    def export_plan(self):
        """导出方案"""
        current_index = self.plans_area.currentIndex()
        if current_index >= 0 and current_index < len(self.current_plans):
            plan = self.current_plans[current_index]
            
            # 选择保存位置
            file_path, _ = QFileDialog.getSaveFileName(
                self, "导出方案", f"{plan['title']}.md", "Markdown files (*.md)"
            )
            
            if file_path:
                try:
                    # 使用增强的导出功能
                    if hasattr(self.app, 'travel_planner'):
                        success = self.app.travel_planner.export_plan_to_markdown(plan, file_path)
                        if success:
                            QMessageBox.information(self, "成功", f"方案已导出到：{file_path}")
                        else:
                            QMessageBox.warning(self, "错误", "导出失败，请稍后重试")
                    else:
                        # 备用导出方法
                        self.export_to_markdown_fallback(plan, file_path)
                        QMessageBox.information(self, "成功", f"方案已导出到：{file_path}")
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"导出失败：{e}")
    
    def export_to_markdown_fallback(self, plan: Dict[str, Any], file_path: str):
        """备用导出方法"""
        content = f"""# {plan['title']}

## 基本信息
- **目的地**：{plan['destination']}
- **天数**：{plan['days']}天
- **预算**：{plan['budget']}元
- **预计费用**：{plan.get('estimated_cost', 0):.0f}元
- **方案类型**：{plan.get('plan_type', '标准型')}

## 详细行程
"""
        
        if 'daily_schedule' in plan:
            for day_info in plan['daily_schedule']:
                content += f"\n### 第{day_info['day']}天\n"
                if 'attractions' in day_info and day_info['attractions']:
                    for attraction in day_info['attractions']:
                        content += f"- **{attraction['name']}** ({attraction['duration']}小时, {attraction['cost']}元)\n"
                else:
                    content += "- 自由安排\n"
        else:
            content += "\n详细行程正在规划中...\n"
        
        if 'accommodation' in plan:
            hotel = plan['accommodation']
            content += f"\n## 住宿推荐\n- {hotel['name']} - {hotel['price']}元/晚\n"
        
        if 'local_food' in plan:
            content += f"\n## 美食推荐\n"
            for food in plan['local_food']:
                content += f"- {food}\n"
        
        if 'tips' in plan:
            content += f"\n## 旅行小贴士\n"
            for tip in plan['tips']:
                content += f"- {tip}\n"
        
        content += f"\n---\n*生成时间：{plan.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}*"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)