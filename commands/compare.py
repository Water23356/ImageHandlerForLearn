import os,cv2,Global
from console import Printer as printer

def execute_function(args):
    image = cv2.imread(args.path1)
    if image is None:
        Global.print("图片1加载失败")
    else:
        Global.program.img1.setImage(image)
        Global.print("图片1加载成功")
        
    image2 = cv2.imread(args.path2)
    if image2 is None:
        Global.print("图片2加载失败")
    else:
        Global.program.img2.setImage(image2)
        Global.print("图片2加载成功")
        
    pass

subcommand = {
    'head' : 'compare',
    'help' : '比较两幅图片',
    'description' : '将两张本地图片加载到窗口',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : 'path1',
            'help' : '图像1路径',
            'type' : str,
        },
        {
            'name' : 'path2',
            'help' : '图像2路径',
            'type' : str,
        }
    )
} 