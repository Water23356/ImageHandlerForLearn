import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import Global
from scipy.signal import convolve2d


def generate_mean_kernel(size):
    """
    生成均值卷积核
    :param size: 卷积核的大小 (正整数)
    :return: 均值卷积核 (numpy.ndarray)
    """
    if size <= 0 or size % 2 == 0:
        raise ValueError("卷积核大小必须是正奇数")
    
    kernel = np.ones((size, size), dtype=np.float32)  # 创建一个 size x size 的矩阵，所有元素为1
    kernel /= size ** 2  # 归一化，使得总和为1
    return kernel

def generate_gaussian_kernel(size, sigma=1.0):
    """
    生成高斯卷积核
    :param size: 卷积核的大小 (正奇数)
    :param sigma: 高斯分布的标准差
    :return: 高斯卷积核 (numpy.ndarray)
    """
    if size <= 0 or size % 2 == 0:
        raise ValueError("卷积核大小必须是正奇数")
    
    # 计算中心点的偏移量
    center = size // 2
    
    # 创建一个 size x size 的矩阵
    kernel = np.zeros((size, size), dtype=np.float32)
    
    # 计算每个位置的高斯权重
    for i in range(size):
        for j in range(size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    
    # 归一化，使得卷积核的总和为1
    kernel /= (2 * np.pi * sigma**2)
    kernel /= np.sum(kernel)  # 确保总和为1
    
    return kernel


# 子线程任务类
class MeanThread(QThread):
    def __init__(self, image, gaussian, coreSize):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.coreSize = coreSize
        self.gaussian = gaussian
        self.signals = Global.ThreadSignals()

    def run(self):
        try:
            # 确保图像是灰度图像
            if len(self.image.shape) == 3:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # 选择卷积核
            if self.gaussian:
                kernel = generate_gaussian_kernel(self.coreSize)
                # kernel = np.array([[1, 2, 1],
                #                    [2, 4, 2],
                #                    [1, 2, 1]]) / 16.0
            else:
                kernel = generate_mean_kernel(self.coreSize)
                # kernel = np.array([[1, 1, 1],
                #                    [1, 1, 1],
                #                    [1, 1, 1]]) / 9.0

            # 应用卷积
            convolved_image = convolve2d(self.image, kernel, mode='same', boundary='fill', fillvalue=0)

            # 确保卷积结果在 [0, 255] 范围内
            convolved_image = np.clip(convolved_image, 0, 255).astype(np.uint8)

            self.signals.finished.emit(convolved_image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"均值模板处理失败: {e}")


# 执行任务的函数
def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    coreSize = args.coreSize
    gaussian = args.gaussian
    if coreSize <3:
        Global.print_error("卷积核大小不应小于3")

    def on_finished(convolved_image):
        Global.program.img2.setImage(convolved_image)
        Global.print("均值模板处理完成")

    def on_error(message):
        Global.print(message)

    thread = MeanThread(image, gaussian, coreSize)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread


# 子命令配置
subcommand = {
    'head': 'mean',
    'help': '均值模板处理',
    'description': '对图像进行均值模板或高斯模板卷积处理',
    'execute': execute_function,
    'subcommands': [],
    'args': (
        {
            'name': ('-c', '--coreSize'),
            'help': '卷积核大小(>=3)',
            'default': 3,
            'type': int,
        },
        {
            'name': ('-g', '--gaussian'),
            'help': '使用高斯均值模板',
            'action': 'store_true',
            'default': False,
        },
    )
}