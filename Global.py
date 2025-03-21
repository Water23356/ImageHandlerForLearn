from main import Program
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import numpy as np

class ThreadSignals(QObject):
    finished = pyqtSignal(np.ndarray)  # 传递处理后的图像
    errorOccurred = pyqtSignal(str)   # 传递错误信息

global program
program:Program = None
global taskThreadRunning
taskThreadRunning = False

def print(message):
    program.cmd.sendMessage(message)
    
    
    

    