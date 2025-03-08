import os
import Global
import cv2


def execute_function(args):
    img = cv2.imread(args.path)
    if args.gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    Global.program.img1.setImage(img)
    if Global.program.img1.image is None:
        Global.print(f"加载图片失败: {args.path}")
        return
    Global.print(f"加载图片成功: {args.path}")
    pass

subcommand = {
    'head' : 'load',
    'help' : '加载图片',
    'description' : '加载原始图片',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : 'path',
            'help' : '图片路径',
            'type' : str,
        },
        {
            'name' :('-g','--gray'),
            'help' : '灰度图',
            'action' : 'store_true',
            'default' : False,
        }
    )
}