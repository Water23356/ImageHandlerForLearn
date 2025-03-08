import os,Global,cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, pyqtSignal, QThread

def display_histogram(histogram):
    """
    使用 Matplotlib 绘制直方图
    :param histogram: 直方图数组
    """
    plt.figure(figsize=(8, 6))
    plt.bar(range(256), histogram, color='gray', width=1.0)
    plt.title("灰度直方图", fontsize=16)
    plt.xlabel("灰度值", fontsize=14)
    plt.ylabel("像素数量", fontsize=14)
    plt.xlim([0, 256])  # 设置 x 轴范围
    plt.grid(True)
    plt.show()
    
def calculate_histogram(image):
    """
    手动计算灰度直方图
    :param image: 灰度图像（numpy数组）
    :return: 直方图数组（大小为256）
    """
    # 初始化直方图数组，大小为256
    histogram = np.zeros(256, dtype=np.int32)
    
    # 遍历图像的每个像素，统计每个灰度值的出现次数
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            gray_value = image[y, x]
            histogram[gray_value] += 1
    
    return histogram

def execute_function(args):
    if args.origin == 'origin':
        img = Global.program.img1.image
    elif args.origin == 'handled':
        img = Global.program.img2.image

    if img is None:
        Global.print(f"未加载图片: {args.origin}")
        return

    # 确保输入灰度图
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      
    hist = calculate_histogram(img)
    # hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    
    display_histogram(hist)
            
       


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


sub_equalize={
    'head' : 'equalize',
    'help' : '直方图均衡化',
    'description' : '对图像进行直方图均衡化',
    'execute' : execute_function_equalize,
    'subcommands': [],
    'args' : (
    )
}


subcommand = {
    'head' : 'hist',
    'help' : '灰度直方图',
    'description' : '显示图像的灰度直方图',
    'execute' : execute_function,
    'subcommands': [sub_equalize],
    'args' : (
        {
            'name': ('-o', '--origin'),
            'help': '查看目标',
            'choices': ['origin', 'handled'],
            'default': 'origin',
            'required': False,
        },
    )
}