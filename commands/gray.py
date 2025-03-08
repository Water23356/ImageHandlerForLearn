import os
import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global


# 自定义信号类
class GrayThreadSignals(QObject):
    finished = pyqtSignal(np.ndarray)  # 传递处理后的图像
    errorOccurred = pyqtSignal(str)  # 传递错误信息


# 子线程任务类
class GrayThread(QThread):
    def __init__(self, image, levels):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.levels = levels
        self.signals = GrayThreadSignals()

    def run(self):
        Global.taskThreadRunning = True
        try:
            # 计算每个灰度级的间隔
            interval = 256 // self.levels
            # 遍历每个像素，将其灰度值映射到新的灰度级
            for y in range(self.image.shape[0]):
                for x in range(self.image.shape[1]):
                    gray = self.image[y, x]
                    new_gray = gray // interval * interval
                    self.image[y, x] = new_gray

            self.signals.finished.emit(self.image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"修改失败: {e}")
        finally:
            Global.taskThreadRunning = False


# 执行任务的函数
def execute_function(args):
    img = Global.program.img1.image
    if img is None:
        Global.print("请先加载图片")
        return
    
    # 确保图像是灰度图像
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    levels = args.levels

    def on_finished(image):
        Global.program.img2.setImage(image)
        Global.print(f"调整灰度级完成: {levels}")

    def on_error(message):
        Global.print(message)

    thread = GrayThread(img, levels)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'gray',
    'help': '调整灰度级',
    'description': '调整灰度级数',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': 'levels',
            'help': '灰度级数',
            'type': int,
        },
    )
}