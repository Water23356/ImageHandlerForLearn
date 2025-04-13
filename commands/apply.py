import os,Global,cv2
import numpy as np
from console import Printer as printer
import commands.create as create_commands
import commands.idft as idft_commands
import commands.dft as dft_commands

##############################################################################


def butterworth_execute_function(args):
    if Global.program.img1.image is None:
        Global.print("未加载图片")
        return
    image = Global.program.img1.image.copy()
    
    # 原图傅里叶变换
    if args.dft:
        image = dft_commands.fft_handle(image)
    
    # 生成Butterworth低通滤波器
    height,width = image.shape[:2]
    cutoff = args.cutoff  # 截止频率
    order = args.order  # 滤波器的阶数
    H = create_commands.butterworth_lowpass_filter(height, width, cutoff, order)
    
    # 应用滤波器
    hanlded = image*H
    
    # 傅里叶逆变换
    if args.idft:
        handled = idft_commands.inverse_fft_from_spectrum(hanlded)
        
    Global.program.img2.setImage(handled)
    pass

def gaussion_highpass_filter_execute_function(args):
    if Global.program.img1.image is None:
        Global.print("未加载图片")
        return
    image = Global.program.img1.image.copy()
    
    # 原图傅里叶变换
    if args.dft:
        image = dft_commands.fft_handle(image)
    
    # 生成Butterworth低通滤波器
    height,width = image.shape[:2]
    cutoff = args.cutoff  # 截止频率
    H = create_commands.gaussion_highpass_filter(height, width, cutoff)
    
    # 应用滤波器
    hanlded = image*H
    
    # 傅里叶逆变换
    if args.idft:
        handled = idft_commands.inverse_fft_from_spectrum(hanlded)
        
    Global.program.img2.setImage(handled)


def laplacian_highpass_filter_execute_function(args):
    if Global.program.img1.image is None:
        Global.print("未加载图片")
        return
    image = Global.program.img1.image.copy()
    
    # 原图傅里叶变换
    if args.dft:
        image = dft_commands.fft_handle(image)
    
    # 生成Butterworth低通滤波器
    height,width = image.shape[:2]
    H = create_commands.laplacian_highpass_filter(height, width)
    
    # 应用滤波器
    hanlded = image*H
    
    # 傅里叶逆变换
    if args.idft:
        handled = idft_commands.inverse_fft_from_spectrum(hanlded)
        
    Global.program.img2.setImage(handled)


##############################################################################

laplac_high_cmd = {
    'head' : 'laplac_high',
    'help' : '应用拉普拉斯高通滤波器', 
    'execute' : laplacian_highpass_filter_execute_function,
    'subcommands': [],
    'args' : (
        {
            'name':('--idft'),
            'help':'是否对结果傅里叶逆变换',
            'action':'store_true',
            'default':False,
        },
        {
            'name':('--dft'),
            'help':'是否对原图傅里叶变换',
            'action':'store_true',
            'default':False,
        }
    )
}

gauss_high_cmd={
    'head' : 'gauss_high',
    'help' : '应用高斯高通滤波器', 
    'execute' : gaussion_highpass_filter_execute_function,
    'subcommands': [],
    'args' : (
        {
            'name':('-c','--cutoff'),
            'help':'截止频率',
            'type':int,
            'default':30,
        },
        {
            'name':('--idft'),
            'help':'是否对结果傅里叶逆变换',
            'action':'store_true',
            'default':False,
        },
        {
            'name':('--dft'),
            'help':'是否对原图傅里叶变换',
            'action':'store_true',
            'default':False,
        }
    )
}

butterworth_cmd = {
    'head' : 'butterworth',
    'help' : '应用butterworth低通滤波器', 
    'description' : '应用butterworth低通滤波器',
    'execute' : butterworth_execute_function,
    'subcommands': [],
    'args' : 
        ({
            'name': ('-o','--order'),
            'help': '滤波器阶数',
            'type': int,
            'default': 1,
        },
        {
            'name':('-c','--cutoff'),
            'help':'截止频率',
            'type':int,
            'default':30,
        },
        {
            'name':('--idft'),
            'help':'是否对结果傅里叶逆变换',
            'action':'store_true',
            'default':False,
        },
        {
            'name':('--dft'),
            'help':'是否对原图傅里叶变换',
            'action':'store_true',
            'default':False,
        }
    )
}


subcommand = {
    'head' : 'apply',
    'help' : '频域处理',
    'description' : '频域处理',
    'execute' : None,
    'subcommands': [
        butterworth_cmd,
        gauss_high_cmd,
        laplac_high_cmd
    ],
    'args' : None
}