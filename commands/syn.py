import os,Global
from console import Printer as printer

def execute_function(args):
    scale = Global.program.img1.scroll_area.scale_factor
    v_scroll_bar = Global.program.img1.scroll_area.verticalScrollBar()
    h_scroll_bar = Global.program.img1.scroll_area.horizontalScrollBar()
    
    handled_v_scroll_bar = Global.program.img2.scroll_area.verticalScrollBar()
    handled_h_scroll_bar = Global.program.img2.scroll_area.horizontalScrollBar()
    
    Global.program.img2.onScaleChanged(scale)
    Global.program.app.processEvents()
    handled_v_scroll_bar.setValue(v_scroll_bar.value())
    handled_h_scroll_bar.setValue(h_scroll_bar.value())
    
    pass

subcommand = {
    'head' : 'syn',
    'help' : '同步窗口',
    'description' : '同步窗口缩放和位置',
    'execute' : execute_function,
    'subcommands': [],
    'args' : (
    )
}