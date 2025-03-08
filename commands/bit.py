import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global


# 自定义信号类
class BitThreadSignals(QObject):
    finished = pyqtSignal(np.ndarray)  # 传递处理后的图像
    errorOccurred = pyqtSignal(str)   # 传递错误信息


# 子线程任务类
class BitThread(QThread):
    def __init__(self, image, layer):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.layer = layer
        self.signals = BitThreadSignals()

    def run(self):
        try:
            # 确保图像是灰度图像
            if len(self.image.shape) == 3:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # 检查分层号是否在有效范围内
            if self.layer < 0 or self.layer > 7:
                self.signals.errorOccurred.emit("分层号必须在0~7之间")
                return

            # 执行比特分层操作
            new_image = self.image.copy()
            new_image = new_image & (1 << self.layer)  # 提取指定比特层

            self.signals.finished.emit(new_image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"比特分层失败: {e}")


# 执行任务的函数
def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return

    layer = args.layer

    def on_finished(new_image):
        Global.program.img2.setImage(new_image)
        Global.print("比特分层完成")

    def on_error(message):
        Global.print(message)

    thread = BitThread(image, layer)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'bit',
    'help': '比特分层',
    'description': '提取图像的指定比特层',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': 'layer',
            'help': '分层号: 0~7',
            'type': int,
        },
    )
}