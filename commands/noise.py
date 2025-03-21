import os,Global,cv2
from console import Printer as printer
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread

class SpNoiseThread(QThread):
    def __init__(self, image, prob, salt,pepper):
        super().__init__()
        self.image = image.copy()  # 避免直接修改原图像
        self.prob = prob
        self.salt = salt
        self.pepper = pepper
        self.signals = Global.ThreadSignals()

    def run(self):
        try:
            # 确保图像是灰度图像
            if len(self.image.shape) == 3:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            # 生成随机矩阵（范围 [0, 1)）
            random_matrix = np.random.rand(*self.image.shape[:2])
            
            # 椒噪声：将随机值 < prob/2 的像素设为 0(默认)
            # 盐噪声：将随机值 > 1 - prob/2 的像素设为 255(默认)
            self.image[random_matrix < self.prob/2] = self.pepper
            self.image[random_matrix > 1 - self.prob/2] = self.salt
            
            self.signals.finished.emit(self.image)  # 发送处理后的图像
        except Exception as e:
            self.signals.errorOccurred.emit(f"均值模板处理失败: {e}")

def sp_execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    
    def on_finished(convolved_image):
        Global.program.img2.setImage(convolved_image)
        Global.print("椒盐噪声添加完毕")

    def on_error(message):
        Global.print(message)

    thread = SpNoiseThread(image, args.prob, args.salt,args.pepper)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread
    pass

sp_noise = {
    'head' : 'sp',
    'help' : '添加椒盐噪声',
    'description' : '添加椒盐噪声',
    'execute' : sp_execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : 'prob',
            'help' : '噪声概率',
            'default' : 0.05,
            'type':float,
        },
        {
            'name' : ('-s','--salt'),
            'help' : '盐值',
            'default' : 255,
            'type':int,
        },
        {
            'name' :('-p','--pepper'),
            'help' : '椒值',
            'default' : 0,
            'type':int,
        },
    )
}

subcommand = {
    'head' : 'noise',
    'help' : '添加噪声',
    'description' : '添加噪声',
    'execute': None,
    'subcommands': [sp_noise],
    'args' : None
}