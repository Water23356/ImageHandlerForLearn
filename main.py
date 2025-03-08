from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit,QLabel,QHBoxLayout,QVBoxLayout
import sys

import matplotlib

from ImageLabel import ZoomImageLabel
from CommandArea import CommandArea
from commands.console import Printer
from commands.parser import init_parser
import Global

class Program:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setGeometry(400, 400, 800, 800)
        self.img1:ZoomImageLabel = None
        self.img2:ZoomImageLabel = None
        self.cmd:CommandArea = None
        self.current_thread = None
        self.initWindow()
        self.initCommand()
        
    def initWindow(self):
        self.img1 = ZoomImageLabel()
        self.img2 = ZoomImageLabel()
        self.cmd = CommandArea(self.app)
        
        # 上部分布局和元素
        self.img1.setTitle("原始图")
        self.img2.setTitle("效果图")
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.img1.widget)
        h_layout.addWidget(self.img2.widget)
        
        #下部分布局和元素
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.cmd)
        
        # 设置上下布局的比例
        v_layout.setStretchFactor(h_layout, 3)
        v_layout.setStretchFactor(self.cmd, 1)
        
        self.window.setLayout(v_layout)
        self.window.show()
        
    def initCommand(self):
        self.parser =  init_parser()
        self.cmd.handleFunc = self.parseCommand

    def parseCommand(self,text):
        Global.print(f"任务状态: {Global.taskThreadRunning}")
        if Global.taskThreadRunning:
            Global.print("请等待当前任务线程完毕...")
            return
        
        try:
            args = self.parser.parse_args(text.split())
            self.execute(args)
        except Exception as e:
            Printer.print(e)
        pass
    
    def execute(self,args):
        # 调用子指令对应的功能函数
        if hasattr(args, 'func'):
            args.func(args)
        else:
            self.parser.print_help()


def main():
    # 设置 Matplotlib 的字体为支持中文的字体
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # Windows 系统
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题

    
    program = Global.program = Program()
    Global.program.cmd.sendMessage("程序运行")
    Global.taskThreadRunning = False
    sys.exit(program.app.exec_())
    pass

if __name__ == '__main__':
    main()


