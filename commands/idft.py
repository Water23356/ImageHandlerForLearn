import numpy as np
import os,Global,cv2
from console import Printer as printer

def inverse_fft_from_spectrum(dft_shift):
    """
    从中心化的频域数据恢复原图
    :param dft_shift: 中心化后的频域数据（复数形式，包含实部和虚部）
    :return: 恢复后的图像（uint8类型）
    """
    # 1. 逆中心化：将低频移回四角
    dft_ishift = np.fft.ifftshift(dft_shift)
    
    # 2. 执行逆傅里叶变换（得到双通道复数结果）
    img_complex = cv2.idft(dft_ishift)
    
    # 3. 计算幅度谱并归一化
    img_back = cv2.magnitude(img_complex[:, :, 0], img_complex[:, :, 1])
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX)
    img_back = img_back.astype(np.uint8)
    
    return img_back



def execute_function(args):
    dft_shift = Global.program.img1.image.copy()
    if dft_shift is None:
        Global.print("未加载图片")
        return
    
    printer.print(len(dft_shift.shape))
    if len(dft_shift.shape) >= 3:
        # 频域全数据
        # 提取实部和虚部
        real_part = dft_shift[:, :, 0]
        imag_part = dft_shift[:, :, 1]
        
        # 计算幅度谱（公式：sqrt(Re^2 + Im^2)）
        magnitude = cv2.magnitude(real_part, imag_part)
        printer.print("计算幅度")
        if args.rad:
            # 仅用相角
            # 计算相角谱（单位：弧度，范围 [-π, π]）
            printer.print("计算相角")
            phase_spectrum = np.arctan2(imag_part, real_part)
            # 重新计算实部和虚部的值
            new_real_part = np.cos(phase_spectrum)
            new_imag_part = np.sin(phase_spectrum)
            # 合并实部和虚部
            dft_shift[:,:,0] = new_real_part
            dft_shift[:,:,1] = new_imag_part
            
        elif args.amplitude:
            # 仅用幅度
            # 仅实部有值, 虚部全0
            zero_phase = np.zeros_like(real_part)  # 全零相位
            new_real_part = magnitude * np.cos(zero_phase)
            new_imag_part = magnitude * np.sin(zero_phase)
            # 合并实部和虚部
            dft_shift[:,:,0] = new_real_part
            dft_shift[:,:,1] = new_imag_part
            
        # 恢复图像
        printer.print("恢复图像")
        img_back = inverse_fft_from_spectrum(dft_shift)
        printer.print("恢复图像完毕")
    else:
        # 频域仅相角或者幅度
        printer.print("单维度频谱")
        if args.rad:
            # 仅用相角, 一维值表示相角
            # 幅度为1
            printer.print("仅用相角")
            new_dft_shift = np.zeros((dft_shift.shape[0], dft_shift.shape[1], 2), dtype=np.float32)
            printer.print("计算实部")
            new_dft_shift[:, :, 0] = np.cos(dft_shift)
            printer.print("计算虚部")
            new_dft_shift[:, :, 1] = np.sin(dft_shift)
            dft_shift = new_dft_shift

        elif args.amplitude:
            # 仅用幅度
            # 基于灰度图创建复数数组, 虚部全0, 实部为幅度
            new_dft_shift = np.zeros((dft_shift.shape[0], dft_shift.shape[1], 2), dtype=np.float32)
            new_dft_shift[:, :, 0] = np.cos(dft_shift)
            dft_shift = new_dft_shift

        # 恢复图像
        printer.print("恢复图像")
        img_back = inverse_fft_from_spectrum(dft_shift)
        printer.print("恢复图像完毕")
            
    
    # 输出结果
    Global.print("傅里叶反变换完成")
    Global.program.img2.setImage(img_back)
    pass

subcommand = {
    'head' : 'idft',
    'help' : '傅里叶反变换',
    'description' : '傅里叶反变换',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name': ('-r', '--rad'),
            'help': '仅用相角',
            'action' : 'store_true',
            'default': False,
        },
        {
            'name': ('-a', '--amplitude'),
            'help': '仅用幅度',
            'action' : 'store_true',
            'default': False,
        }
    )
}