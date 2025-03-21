import os
import cv2
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import numpy as np
import Global
from console import Printer as printer


# 自定义信号类
class SaveThreadSignals(QObject):
    finished = pyqtSignal(str)  # 传递保存结果信息
    errorOccurred = pyqtSignal(str)  # 传递错误信息


# 子线程任务类
class SaveThread(QThread):
    def __init__(self, image, path,saveAsNpy):
        super().__init__()
        self.image = image
        self.path = path
        self.saveAsNpy = saveAsNpy
        self.signals = SaveThreadSignals()

    def run(self):
        Global.taskThreadRunning = True
        try:
            if self.saveAsNpy:
                np.save(self.path, self.image)
                self.signals.finished.emit(f"保存成功: {self.path}")
            else:
                cv2.imwrite(self.path, self.image)
                self.signals.finished.emit(f"保存成功: {self.path}")
        except Exception as e:
            self.signals.errorOccurred.emit(f"保存失败: {e}")
        finally:
            Global.taskThreadRunning = False


# 执行任务的函数
def execute_function(args):
    if args.origin == 'origin':
        img = Global.program.img1.image
    elif args.origin == 'handled':
        img = Global.program.img2.image

    if img is None:
        Global.print(f"未加载图片: {args.origin}")
        return

    path = args.file

    def on_finished(message):
        Global.print(message)

    def on_error(message):
        Global.print(message)

    thread = SaveThread(img, path,args.npy)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'save',
    'help': '保存',
    'description': '将图片保存到本地',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': ('-o', '--origin'),
            'help': '保存目标',
            'choices': ['origin', 'handled'],
            'default': 'origin',
            'required': False,
        },
        {
            "name": ('-f', '--file'),
            "help": "保存文件路径",
            "type": str,
            "required": True,
        },
        {
            "name": ('-n', '--npy'),
            "help": "保存为npy格式",
            "action": "store_true",
            "default": False
        }
    )
}