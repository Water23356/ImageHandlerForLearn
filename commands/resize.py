import os
import threading
import cv2
from console import Printer as printer
import numpy as np
import Global
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# 自定义信号类
class ThreadSignals(QObject):
    finished = pyqtSignal(object)  # 传递缩放后的图像数据


# 子线程任务类
class ResizeThread(QThread):
    def __init__(self,image,width,height,scale):
        super().__init__()
        self.image = image
        self.width = width
        self.height = height
        self.scale = scale
        self.signals = ThreadSignals()

    def run(self):
        Global.taskThreadRunning = True
        try:
            
            if len(self.image.shape) == 2:
                newImg = np.full((int(self.height), int(self.width)),255, dtype=np.uint8)
            else:
                newImg = np.zeros((int(self.height), int(self.width), self.channels), dtype=np.uint8)            
                
            # 最近邻插值算法
            for i in range(int(self.height)):
                for j in range(int(self.width)):
                    x = int(i / self.scale)
                    y = int(j / self.scale)
                    newImg[i, j] = self.image[x, y]
            
            self.signals.finished.emit(newImg)  # 发送结果
            Global.taskThreadRunning = False
            
        except Exception as e:
            print(f"线程错误: {e}")
            Global.taskThreadRunning = False
            

def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("请先加载图片")
        return
    
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    else:
        height, width, channels = image.shape
        
    Global.print(f"原始大小: 宽={width} 高={height} 通道={channels}")
    height =  height * args.scale
    width = width * args.scale
    Global.print(f"修改大小: 宽={width} 高={width} 通道={channels}")
    
    def end(result):
        Global.program.img2.setImage(result)
        Global.print(f"缩放完成: {args.scale}:{width}x{height}")
        
    
    thread = Global.current_thread = ResizeThread(image,width,height,args.scale)
    thread.signals.finished.connect(end)
    thread.start()
    pass

subcommand = {
    'head' : 'resize',
    'help' : '缩放',
    'description' : '将原图进行缩放采样',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : 'scale',
            'help' : '缩放大小',
            'type' : float,
            'default' : 1.0
        }
    )
}