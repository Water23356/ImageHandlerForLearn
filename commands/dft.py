import os,cv2,Global
import numpy as np
from console import Printer as printer
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from matplotlib import pyplot as plt

def fft_handle(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    img_float32 = np.float32(image)
    dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    return dft_shift



class HandleThread(QThread):
    def __init__(self,image,show_rad,show_amplitude):
        super().__init__()
        self.image = image.copy()
        self.show_rad = show_rad
        self.show_amplitude = show_amplitude
        self.signals = Global.ThreadSignals()

    def run(self):
        try:
            # 得到傅里叶变换结果(已平移至中心)
            dft_shift = fft_handle(self.image)
            
            # 提取实部和虚部
            real_part = dft_shift[:, :, 0]
            imag_part = dft_shift[:, :, 1]

            # 计算幅度谱（公式：sqrt(Re^2 + Im^2)）
            magnitude = cv2.magnitude(real_part, imag_part)
            
            # 计算相角谱（单位：弧度，范围 [-π, π]）
            phase_spectrum = np.arctan2(imag_part, real_part)


            if self.show_rad:
                # 显示相角谱
                self.signals.finished.emit(phase_spectrum)  # 发送处理后的图像
            elif self.show_amplitude:
                # 显示幅度谱    
                self.signals.finished.emit(magnitude)  # 发送处理后的图像
            else:
                # 显示双通道结果
                self.signals.finished.emit(dft_shift)  # 发送处理后的图像

        except Exception as e:
            self.signals.errorOccurred.emit(f"傅里叶变换失败: {e}")

def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    
    def on_finished(convolved_image):
        Global.program.img2.setImage(convolved_image)
        Global.print("傅里叶变换完成")

    def on_error(message):
        Global.print(message)

    thread = HandleThread(image,args.rad,args.amplitude)
    thread.signals.finished.connect(on_finished)
    thread.signals.errorOccurred.connect(on_error)
    thread.start()
    Global.current_thread = thread
    pass

subcommand = {
    'head' : 'dft',
    'help' : '傅里叶变换',
    'description' : '傅里叶变换, 仅灰度',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name': ('-r', '--rad'),
            'help': '显示相角',
            'action' : 'store_true',
            'default': False,
        },
        {
            'name': ('-a', '--amplitude'),
            'help': '显示幅度',
            'action' : 'store_true',
            'default': False,
        }
    )
}