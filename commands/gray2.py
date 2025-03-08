import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global


# 自定义信号类
class Gray2ThreadSignals(QObject):
    finished = pyqtSignal(np.ndarray)  # 传递处理后的图像
    errorOccurred = pyqtSignal(str)  # 传递错误信息


# 子线程任务类
class Gray2Thread(QThread):
    def __init__(self, image, threshold):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.threshold = threshold
        self.signals = Gray2ThreadSignals()

    def run(self):
        try:
            # 确保图像是灰度图像
            if len(self.image.shape) == 3:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # 灰度二值化处理
            _, new_image = cv2.threshold(self.image, self.threshold, 255, cv2.THRESH_BINARY)

            self.signals.finished.emit(new_image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"灰度二值化失败: {e}")


# 执行任务的函数
def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("请先加载图片")
        return

    threshold = args.threshold

    def on_finished(new_image):
        Global.program.img2.setImage(new_image)
        Global.print(f"灰度二值化完成: 阈值={threshold}")

    def on_error(message):
        Global.print(message)

    thread = Gray2Thread(image, threshold)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'gray2',
    'help': '灰度二值化',
    'description': '高于一定阈值的灰度值设为255，低于阈值的灰度值设为0',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': 'threshold',
            'help': '阈值',
            'type': float,
        },
    )
}