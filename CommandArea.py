from datetime import datetime
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QVBoxLayout,QScrollArea
from PyQt5.QtCore import Qt

SCALE_UNIT = 6

class RollScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        angle/=SCALE_UNIT
        v_scroll_bar = self.verticalScrollBar()
        v_scroll_bar.setValue(v_scroll_bar.value() - int(angle))
    

class CommandArea(QWidget):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.initUI()
        self.handleFunc = None  # 指令处理接口

    def initUI(self):
        # 创建 QLineEdit 作为命令输入框
        self.line_edit = QLineEdit(self)
        self.line_edit.returnPressed.connect(self.handle_command)

        # 创建 QLabel 用于显示命令消息
        self.message_label = QLabel(self)
        
        self.message_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.content_widget = QWidget()
        self.scroll_area = RollScrollArea()
        self.scroll_area.setWidget(self.message_label)
        self.scroll_area.setWidgetResizable(True)

        # 创建布局并添加组件
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        
        # 设置窗口属性
        # self.setWindowTitle('命令输入与消息显示')
        # self.setGeometry(100, 100, 300, 200)
        # self.show()

    def handle_command(self):
        # 获取输入框中的文本
        command = self.line_edit.text()
        self.line_edit.clear()

        self.sendMessage(command)
        if self.handleFunc: # 指令处理接口
            self.handleFunc(command)
        
        
    def sendMessage(self,message):
        """
        发送消息
        """
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S:") + "{:03}".format(current_time.microsecond // 1000)
        message = f"[{formatted_time}]: {message}"
        current_message = self.message_label.text()
        if current_message:
            new_message = f"{current_message}\n{message}"
        else:
            new_message = message
        self.message_label.setText(new_message)
        
        # 刷新界面
        self.app.processEvents()
        
        # 将滚动条的值设置为最大值，使其置于最底部
        v_scroll_bar = self.scroll_area.verticalScrollBar()
        v_scroll_bar.setValue(v_scroll_bar.maximum())
