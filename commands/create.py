import os,Global,cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from console import Printer as printer


def fill_execute_function(args):
    output = np.full((args.height,args.width),args.value,dtype=np.uint8)
    Global.program.img1.setImage(output)
    Global.print("填充完成")
    pass


fill_cmd = {
    'head' : 'fill',
    'help' : '填充图像', 
    'description' : '填充图像',
    'execute' : fill_execute_function,
    'subcommands': [],
    'args' : (
        {
            'name': 'width',
            'help': '宽度',
            'type': int,
            'default': 1,
        },
        {
            'name': 'height',
            'help': '高度',
            'type': int,
            'default': 1,
        },
        {
            'name': ('-v','--value'),
            'help': '填充值',
            'type': int,
            'default': 0,
        },
    )
}

subcommand = {
    'head' : 'create',
    'help' : '创建图像',
    'description' : '创建图像',
    'execute' : None,
    'subcommands': [fill_cmd],
    'args' : None
}