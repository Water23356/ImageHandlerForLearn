import argparse
import os
import sys
import importlib
from commands.console import Printer as printer

class Parser(argparse.ArgumentParser):
    def error(self, message):
        printer.print_error(message)


def init_parser():
    """初始化命令行参数解析器并注册子指令"""
    # 创建主解析器
    parser = Parser(description="主命令行解析器",exit_on_error=False,add_help=False)
    # 添加子解析器
    subparsers = parser.add_subparsers(title="子指令", dest="subcommand")
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 遍历同级目录中的所有文件
    for filename in os.listdir(current_dir):
        # 检查文件是否为 .py 文件且不是主程序文件
        if filename.endswith('.py') and filename != os.path.basename(__file__):
            # 去除文件扩展名，获取模块名
            module_name = filename[:-3]
            try:
                # 将当前目录添加到系统路径，以便能够导入模块
                sys.path.append(current_dir)
                # 动态导入模块
                module = importlib.import_module(module_name)
                if hasattr(module, 'subcommand'):
                    subcommand : dict = module.subcommand.copy()
                    register_subparser(subparsers,subcommand)

            except ModuleNotFoundError:
                printer.print_error(f"警告：无法导入模块 {module_name}")
            except Exception as e:
                printer.print_error(f"警告：无法导入模块 {module_name}: {e}")

    return parser


def register_subparser(subparsers,subcommand):
    head = subcommand["head"]
    func = subcommand["execute"]
    args = subcommand["args"]
    subs = subcommand["subcommands"]
    
    del subcommand["head"]
    del subcommand["execute"]
    del subcommand["args"]
    del subcommand["subcommands"]
    subparser:argparse.ArgumentParser = subparsers.add_parser(head, **subcommand) # type: ignore
    
    # 注册子指令的参数
    if(not isinstance(args,tuple)):
        name_or_flags = args["name"]
        del args["name"]
        if isinstance(name_or_flags,tuple):
            subparser.add_argument(*name_or_flags, **args)
        else:
            subparser.add_argument(name_or_flags, **args)
    else:
        for arg in args:
            name_or_flags = arg["name"]
            del arg["name"]
            if isinstance(name_or_flags,tuple):
                subparser.add_argument(*name_or_flags, **arg)
            else:
                subparser.add_argument(name_or_flags, **arg)
    
    # 设置子指令的默认执行函数
    subparser.set_defaults(func=func)
    
    # 递归注册子指令
    newSubparsers = subparser.add_subparsers(title="子指令", dest="subcommand")
    for sub in subs:
        register_subparser(newSubparsers,sub)
    pass