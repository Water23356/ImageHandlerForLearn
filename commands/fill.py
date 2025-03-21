import os,Global,cv2
from console import Printer as printer

def execute_function(args):
    if args.operate == 'origin':
        image = Global.program.img1.image.copy()
    elif args.operate == 'handled':
        image = Global.program.img2.image.copy()

    if image is None:
        Global.print("未加载图片")
        return

    x = args.x
    y = args.y
    width = args.width
    height = args.height

    if x < 0 or y < 0 or x >= image.shape[1] or y >= image.shape[0]:
        Global.print("填充位置超出图像范围")
        return
    
    if width < 0 or height < 0 or x + width > image.shape[1] or y + height > image.shape[0]:
        Global.print("填充区域超出图像范围")
        return
    
    if image.ndim == 3:
        # 彩色图像
        image[y:y+height, x:x+width, args.chanel] = args.value
    else:
        # 灰度图像
        image[y:y+height, x:x+width] = args.value
    
    Global.print("填充完成: x={}, y={}, width={}, height={}, value={}".format(x, y, width, height, args.value))
    if args.operate == 'origin':
        Global.program.img1.setImage(image)
    elif args.operate == 'handled':
        Global.program.img2.setImage(image)
    
    pass

subcommand = {
    'head' : 'fill',
    'help' : '填充图像',
    'description' : '填充图像',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : ('-o','--operate'),
            'help' : '操作目标',
            'default' : 'origin',
            'choices' : ['origin', 'handled'],
        },
        {
            'name': ('--x'),
            'help': '填充起始x',
            'type': int,
            'default': 0,
        },
        {
            'name': ('--y'),
            'help': '填充起始y',
            'type': int,
            'default': 0,
        },
        {
            'name': ('--width'),
            'help': '填充宽度',
            'type': int,
            'default': 1,
        },
        {
            'name': ('--height'),
            'help': '填充高度',
            'type': int,
            'default': 1,
        },
        {
            'name': ('-v','--value'),
            'help': '填充值',
            'type': int,
            'default': 0,
        },
        {
            'name':('-c','--chanel'),
            'help':'填充通道',
            'type':int,
            'default':0,
            'choices':[0,1,2]
        }
    )
}