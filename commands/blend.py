import os,Global
import numpy as np
from console import Printer as printer

def execute_function(args):
    image1 = Global.program.img1.image
    image2 = Global.program.img2.image
    
    if image1 is None:
        Global.print("未加载图片: origin")
        return
    if image2 is None:
        Global.print("未加载图片: handled")
        return
    
    if args.operation == 'add':
        result = image1 + image2
    elif args.operation == 'sub':
        result = image1 - image2
    elif args.operation == 'mul':
        result = image1 * image2
    elif args.operation == 'div':
        result = image1 / image2

    result = np.clip(result, 0, 255).astype(np.uint8)
    Global.program.img2.setImage(result)
    Global.print("混合完成")
    pass

subcommand = {
    'head' : 'blend',
    'help' : '混合原图和处理图',
    'description' : '按照指定操作混合原图和处理图',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
        {
            'name' : 'operation',
            'help' : '混合操作',
            'type' : str,
            'choices' : ['add', 'sub', 'mul','div'],
        }
    )
}