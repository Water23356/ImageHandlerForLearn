import os,Global,cv2
import numpy as np
from console import Printer as printer
from scipy.signal import convolve2d

def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    vertical = args.vertical
    
    if vertical :
        kernel = [[-1,0,1],
                [-2,0,2],
                [-1,0,1]] 
    else:
        kernel = [[-1,-2,-1],
                [0,0,0],
                [1,2,1]]
    
     # 应用卷积
    convolved_image = convolve2d(image, kernel, mode='same', boundary='fill', fillvalue=0)

    # 确保卷积结果在 [0, 255] 范围内
    convolved_image = np.clip(convolved_image, 0, 255).astype(np.uint8)
        
    Global.program.img2.setImage(convolved_image)
    pass

subcommand = {
    'head' : 'sobel',
    'help' : 'sobel 算子卷积',
    'description' : 'sobel 锐化',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : ('-v','--vertical'),
            'help' : '使用垂直方向的 sobel 算子',
            'action' : 'store_true',
            'default' : False,
        }
    )
}