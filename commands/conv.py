import os,Global
from scipy.signal import convolve2d
import numpy as np
from console import Printer as printer

def execute_function(args):
    image = Global.program.img1.image
    if image is None:
        Global.print("未加载图片")
        return
    
    # 将输入转换为二维数组
    printer.print(f"origin: {args.kernel}", )
    kernel_str = args.kernel
    kernel = []
    for row in kernel_str:
        elements = list(map(int, row.split(',')))  # 拆分为整数列表
        kernel.append(elements)
    kernel = np.array(kernel, dtype=np.float32)    # 转换为NumPy矩阵
    
    # 验证是否为矩阵
    if kernel.ndim != 2:
        Global.print("输入的参数不是2维矩阵")
        return
    
    # 验证是否为奇数列（避免中心偏移）
    rows, cols = kernel.shape
    if rows % 2 == 0 or cols % 2 == 0:
        raise ValueError("卷积核行列数必须为奇数")
    
    # 可选归一化处理
    if args.normalize:
        kernel = kernel / np.sum(kernel)
    
    # 应用卷积
    convolved_image = convolve2d(image, kernel, mode='same', boundary='fill', fillvalue=0)

    # 确保卷积结果在 [0, 255] 范围内
    convolved_image = np.clip(convolved_image, 0, 255).astype(np.uint8)
        
    Global.program.img2.setImage(convolved_image)
    pass

subcommand = {
    'head' : 'conv',
    'help' : '卷积',
    'description' : '卷积处理',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' :('-k','--kernel'),
            'help' : '卷积核参数，每行用逗号分隔，多行用空格分隔。例如：-k 1,0,-1 0,0,0 -1,0,1',
            'nargs':'+',
            'type': str,
            'required':True,
        },
        {
            'name' :('-n','--normalize'),
            'help' : '是否归一化卷积核',
            'action': 'store_true',
            'default': False,
        }
    )
}