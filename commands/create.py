import os,Global,cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from console import Printer as printer

def laplacian_highpass_filter(height, width):
    """
    生成拉普拉斯高通滤波器
    :param shape: 滤波器的形状
    :return: 拉普拉斯高通滤波器
    """
    rows, cols = height, width
    crow, ccol = rows // 2, cols // 2
    x = np.linspace(-ccol, ccol, cols)
    y = np.linspace(-crow, crow, rows)
    x, y = np.meshgrid(x, y)
    d = x**2 + y**2
    H = -4*np.pi**2*d
    mask = np.dstack([H, H])
    # H = H / np.max(np.abs(H)) 归一化处理
    return mask

def gaussion_highpass_filter(height, width, cutoff):
    """
    生成高斯高通滤波器
    :param shape: 滤波器的形状
    :param cutoff: 截止频率
    :return: 高通滤波器
    """
    rows, cols = height, width
    crow, ccol = rows // 2, cols // 2
    x = np.linspace(-ccol, ccol, cols)
    y = np.linspace(-crow, crow, rows)
    x, y = np.meshgrid(x, y)
    d = np.sqrt(x**2 + y**2)
    H = 1 - np.exp(-(d**2) / (2 * (cutoff**2)))
    mask = np.dstack([H, H])
    return mask


# 生成Butterworth低通滤波器
def butterworth_lowpass_filter(height, width, cutoff, order):
    """
    生成Butterworth低通滤波器
    :param shape: 滤波器的形状
    :param cutoff: 截止频率
    :param order: 滤波器的阶数
    :return: 低通滤波器
    """
    rows, cols = height, width
    crow, ccol = rows // 2, cols // 2
    x = np.linspace(-ccol, ccol, cols)
    y = np.linspace(-crow, crow, rows)
    x, y = np.meshgrid(x, y)
    d = np.sqrt(x**2 + y**2)
    H = 1 / (1 + (d / cutoff)**(2*order))
    mask = np.dstack([H, H])
    return mask

##############################################################################

def fill_execute_function(args):
    output = np.full((args.height,args.width),args.value,dtype=np.uint8)
    Global.program.img1.setImage(output)
    Global.print("填充完成")
    pass

def butterworth_execute_function(args):
    fromOrigin = args.fromOrigin
    if fromOrigin:
        image = Global.program.img1.image
        if image is None:
            Global.print("未加载图片")
            return
        height,width = image.shape[:2]
    else:
        height,width = args.height,args.width
        
    # 生成Butterworth低通滤波器
    cutoff = args.cutoff  # 截止频率
    order = args.order  # 滤波器的阶数
    H = butterworth_lowpass_filter(height, width, cutoff, order)
    
    if fromOrigin:
        Global.program.img2.setImage(H)
    else:
        Global.program.img1.setImage(H)
    pass

def gaussion_highpass_filter_execute_function(args):
    fromOrigin = args.fromOrigin
    if fromOrigin:
        image = Global.program.img1.image
        if image is None:
            Global.print("未加载图片")
            return
        height,width = image.shape[:2]
    else:
        height,width = args.height,args.width
        
    # 生成高斯高通滤波器
    cutoff = args.cutoff  # 截止频率
    H = gaussion_highpass_filter(height, width, cutoff)
    
    if fromOrigin:
        Global.program.img2.setImage(H)
    else:
        Global.program.img1.setImage(H)
    pass


def laplacian_highpass_filter_execute_function(args):
    fromOrigin = args.fromOrigin
    if fromOrigin:
        image = Global.program.img1.image
        if image is None:
            Global.print("未加载图片")
            return
        height,width = image.shape[:2]
    else:
        height,width = args.height,args.width
        
    H = laplacian_highpass_filter(height, width)
    
    if fromOrigin:
        Global.program.img2.setImage(H)
    else:
        Global.program.img1.setImage(H)
    pass


##############################################################################

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
        }
    )
}

butterworth_cmd = {
    'head' : 'butterworth',
    'help' : '创建butterworth低通滤波器',
    'description' : '创建butterworth低通滤波器, ',
    'execute' : butterworth_execute_function,
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
            'name': ('-o','--fromOrigin'),
            'help': '以源图为模板, 启用时长宽参数无效',
            'action':'store_true',
            'default': False,
        },
        {
            'name': ('--order'),
            'help': '滤波器阶数',
            'type': int,
            'default': 1,
        },
        {
            'name':('--cutoff'),
            'help':'截止频率',
            'type':int,
            'default':30,
        }
    )
}

gaussion_highpass_filter_cmd = {
    'head' : 'guass_high', 
    'help' : '创建高斯高通滤波器',
    'description' : '创建高斯高通滤波器',
    'execute' : gaussion_highpass_filter_execute_function,
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
            'name': ('-o','--fromOrigin'),
            'help': '以源图为模板, 启用时长宽参数无效',
            'action':'store_true',
            'default': False,
        },
        {
            'name':('--cutoff'),
            'help':'截止频率',
            'type':int,
            'default':30,
        }
    )
}

laplacian_highpass_filter_cmd = {
    'head' : 'laplacian_high',
    'help' : '创建拉普拉斯高通滤波器',
    'description' : '创建拉普拉斯高通滤波器',
    'execute' : laplacian_highpass_filter_execute_function,
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
            'name': ('-o','--fromOrigin'),
            'help': '以源图为模板, 启用时长宽参数无效',
            'action':'store_true',
            'default': False,
        }
    )
}

subcommand = {
    'head' : 'create',
    'help' : '创建图像',
    'description' : '创建图像',
    'execute' : None,
    'subcommands': [
        fill_cmd,
        butterworth_cmd,
        gaussion_highpass_filter_cmd,
        laplacian_highpass_filter_cmd
    ],
    'args' : None
}