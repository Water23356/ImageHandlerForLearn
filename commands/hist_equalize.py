import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global


# 自定义信号类
class HistEqualizeThreadSignals(QObject):
    finished = pyqtSignal(np.ndarray)  # 传递处理后的图像
    errorOccurred = pyqtSignal(str)   # 传递错误信息


# 子线程任务类
class HistEqualizeThread(QThread):
    def __init__(self, image):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.signals = HistEqualizeThreadSignals()

    def run(self):
        try:
            # 确保图像是灰度图像
            if len(self.image.shape) == 3:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # 初始化直方图数组，大小为256
            hist = np.zeros(256, dtype=np.int32)
            total_pixels = self.image.shape[0] * self.image.shape[1]

            # 遍历图像的每个像素，统计每个灰度值的出现次数
            for y in range(self.image.shape[0]):
                for x in range(self.image.shape[1]):
                    gray_value = self.image[y, x]
                    hist[gray_value] += 1

            # 计算分布函数（归一化直方图）
            hist = hist / total_pixels

            # 计算累计分布函数
            cdf = np.cumsum(hist)

            # 计算映射表
            map_table = (cdf * 255).astype(np.uint8)

            # 应用映射表
            new_image = map_table[self.image]

            self.signals.finished.emit(new_image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"直方图均衡化失败: {e}")


# 执行任务的函数
def execute_function_equalize(args):
    image = Global.program.img1.image

    if image is None:
        Global.print(f"未加载图片: {args.origin}")
        return

    def on_finished(new_image):
        Global.program.img2.setImage(new_image)
        Global.print("直方图均衡化完成")

    def on_error(message):
        Global.print(message)

    thread = HistEqualizeThread(image)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread
