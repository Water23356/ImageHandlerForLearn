import os,Global
from console import Printer as printer

def execute_function(args):
    origin = Global.program.img1.image.copy()
    handled = Global.program.img2.image.copy()
    
    Global.program.img1.setImage(handled)
    Global.program.img2.setImage(origin)
    
    pass

subcommand = {
    'head' : 'exc',
    'help' : '交换两幅图像位置',
    'description' : '交换预览图像',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
    )
}