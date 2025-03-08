import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global


# 自定义信号类
class LinearThreadSignals(QObject):
    finished = pyqtSignal(np.ndarray)  # 传递处理后的图像
    errorOccurred = pyqtSignal(str)   # 传递错误信息


# 子线程任务类
class LinearThread(QThread):
    def __init__(self, image, a, b):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.a = a
        self.b = b
        self.signals = LinearThreadSignals()

    def run(self):
        try:
            # 确保图像是灰度图像
            if len(self.image.shape) == 3:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # 执行线性运算：f(x) = a * x + b
            self.image = np.clip(self.a * self.image + self.b, 0, 255).astype(np.uint8)

            self.signals.finished.emit(self.image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"线性运算失败: {e}")


# 执行任务的函数
def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return

    a = args.a
    b = args.b

    def on_finished(new_image):
        Global.program.img2.setImage(new_image)
        Global.print("线性运算完成")

    def on_error(message):
        Global.print(message)

    thread = LinearThread(image, a, b)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'linear',
    'help': '线性运算',
    'description': '对灰度图进行线性运算',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': ('-a','--a'),
            'help': '线性运算的 a 参数',
            'type': float,
            'default': 1,
        },
        {
            'name': ('-b','--b'),
            'help': '线性运算的 b 参数',
            'type': float,
            'default': 0,
        }
    )
}