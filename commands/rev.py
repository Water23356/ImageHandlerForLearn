import os,Global,cv2
import numpy as np
from console import Printer as printer

def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    
    if image.ndim == 3:
        for i in range(3):
            image[:,:,i] = 255 - image[:,:,i]
    else:
        image = 255 - image
        
    Global.program.img2.setImage(image)
    Global.print("反相完成")
    pass

subcommand = {
    'head' : 'rev',
    'help' : '反相',
    'description' : '反相处理',
    'execute' : execute_function,
    'subcommands': [],
    'args' : None
}