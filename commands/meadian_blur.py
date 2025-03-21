import os,Global,cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from console import Printer as printer

class HandleThread(QThread):
    def __init__(self,image,coreSize):
        super().__init__()
        self.image = image.copy()
        self.coreSize = coreSize
        self.signals = Global.ThreadSignals()

    def handle(self):
        """
        手动中值滤波实现
        """
        # 输入检查
        if self.coreSize % 2 == 0:
            raise ValueError("卷积核大小必须为奇数.")
        
        h, w = self.image.shape[:2]
        pad = self.coreSize // 2    # 获取边缘填充大小
        denoised = np.zeros_like(self.image) # 创建一个与原始图像大小相同的零数组
        
        # 边缘填充方式
        # 1. 复制边缘像素 : BORDER_REPLICATE
        # 2. 固定值填充 : BORDER_CONSTANT
        # 3. 镜像填充 : BORDER_REFLECT
        padded = cv2.copyMakeBorder(self.image, pad, pad, pad, pad, cv2.BORDER_CONSTANT,0) # 零填充后的图像(用于卷积遍历)
        
        # 遍历每个像素
        for i in range(h):
            for j in range(w):
                # 提取 卷积核 区域
                region = padded[i:i+self.coreSize, j:j+self.coreSize]
                # 计算中值并赋值
                denoised[i, j] = np.median(region)
        return denoised

    def run(self):
        try:
            # 使用内置函数进行均值滤波处理
            self.image = cv2.medianBlur(self.image,self.coreSize)
            # 使用手动实现进行
            #self.image = self.handle()
            # 发送处理后的图像
            self.signals.finished.emit(self.image)
            
        except Exception as e:
            self.signals.errorOccurred.emit(f"中值滤波处理失败: {e}")
        
    

def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    coreSize = args.coreSize
    if coreSize <3:
        Global.print_error("卷积核大小不应小于3")

    def on_finished(convolved_image):
        Global.program.img2.setImage(convolved_image)
        Global.print("中值滤波处理完成")

    def on_error(message):
        Global.print(message)

    thread = HandleThread(image, coreSize)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread
    pass

subcommand = {
    'head' : 'mbulr',
    'help' : '中值滤波',
    'description' : '中值滤波处理',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : ('-c','--coreSize'),
            'help': '卷积核大小(>=3)',
            'default': 3,
            'type': int,
        }
    )
}