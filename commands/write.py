import os
import cv2
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global
from console import Printer as printer


# 自定义信号类
class WriteThreadSignals(QObject):
    finished = pyqtSignal(str)  # 传递保存结果信息
    errorOccurred = pyqtSignal(str)  # 传递错误信息


# 子线程任务类
class WriteThread(QThread):
    def __init__(self, image, path, mode):
        super().__init__()
        self.image = image
        self.path = path
        self.mode = mode
        self.signals = WriteThreadSignals()

    def run(self):
        Global.taskThreadRunning = True
        image = self.image
        try:
            with open(self.path, 'w') as f:
                if len(self.image.shape) == 3:
                    height, width, channel = self.image.shape
                    for y in range(height):
                        for x in range(width):
                            if self.mode == 'all':
                                f.write(f"({image[y,x,2]},{image[y,x,1]},{image[y,x,0]},)")
                            elif self.mode == 'r':
                                f.write(f"{image[y,x,2]},")
                            elif self.mode == 'g':
                                f.write(f"{image[y,x,1]},")
                            elif self.mode == 'b':
                                f.write(f"{image[y,x,0]},")
                            else:
                                self.signals.errorOccurred.emit("未知的模式")
                                return
                        f.write('\n')
                else:
                    height, width = self.image.shape
                    for y in range(height):
                        for x in range(width):
                            f.write(f"{image[y,x]},")
                        f.write('\n')
                f.flush()
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

    mode = args.channel
    path = args.file

    def on_finished(message):
        Global.print(message)

    def on_error(message):
        Global.print(message)

    thread = WriteThread(img, path, mode)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'write',
    'help': '写入通道值',
    'description': '向文件写入图片通道值',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': ('-c', '--channel'),
            'help': '通道选项',
            'choices': ['red', 'green', 'blue', 'all'],
            'default': 'all',
            'required': False,
        },
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
    )
}