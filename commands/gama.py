import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global


# 自定义信号类
class GammaThreadSignals(QObject):
    finished = pyqtSignal(np.ndarray)  # 传递处理后的图像
    errorOccurred = pyqtSignal(str)   # 传递错误信息


# 子线程任务类
class GammaThread(QThread):
    def __init__(self, image, c, y):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.c = c
        self.y = y
        self.signals = GammaThreadSignals()

    def run(self):
        try:
            # 确保图像是灰度图像
            if len(self.image.shape) == 3:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # 执行伽马变换：s = c * r^y
            # 使用 NumPy 的矢量化操作来加速计算
            new_image = self.c * (self.image / 255.0) ** self.y
            new_image = np.clip(new_image * 255, 0, 255).astype(np.uint8)  # 确保结果在 [0, 255] 范围内

            self.signals.finished.emit(new_image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"伽马变换失败: {e}")


# 执行任务的函数
def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return

    c = args.c
    y = args.y

    def on_finished(new_image):
        Global.program.img2.setImage(new_image)
        Global.print("伽马变换完成")

    def on_error(message):
        Global.print(message)

    thread = GammaThread(image, c, y)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'gama',
    'help': '伽马变换',
    'description': 's = c * r ^ y',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': ('-c', '--c'),
            'help': 'c 参数',
            'type': float,
            'default': 1,
        },
        {
            'name': ('-y', '--y'),
            'help': 'y 参数',
            'type': float,
            'default': 1,
        }
    )
}