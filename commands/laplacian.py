import os,Global
import numpy as np
from console import Printer as printer
from scipy.signal import convolve2d

def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    
    if args.diagonal:
        kernel = np.array([[0, 1, 0],
                           [1, -4, 1],
                           [0, 1, 0]])
    else:
        kernel = np.array([[1, 1, 1],
                           [1, -8, 1],
                           [1, 1, 1]])
    
    convolved_image = convolve2d(image, kernel, mode='same', boundary='fill', fillvalue=0)
    
    # 确保卷积结果在 [0, 255] 范围内
    convolved_image = np.clip(convolved_image, 0, 255).astype(np.uint8)
    Global.program.img2.setImage(convolved_image)
    Global.print("拉普拉斯锐化完成")
    pass

subcommand = {
    'head' : 'laplacian',
    'help' : '拉普拉斯锐化',
    'description' : '通过拉普拉斯算子锐化图像',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : ('-d','--diagonal'),
            'help' : '使用对角邻域版本算子',
            'action' : 'store_true',
            'required' : False,
        }
    )
}