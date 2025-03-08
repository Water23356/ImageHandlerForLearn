from rich import console
from rich import console

class Printer:
    _console = console.Console()

    @staticmethod
    def print(text, style="bold white"):
        Printer._console.print(text, style=style)

    @staticmethod
    def print_error(text):
        Printer._console.print(text, style="bold red")

    @staticmethod
    def print_warning(text):
        Printer._console.print(text, style="bold yellow")

    @staticmethod
    def print_success(text):
        Printer._console.print(text, style="bold green")

    def print_info(text):
        Printer._console.print(text, style="bold blue")
        
    def print_log(text):
        Printer._console.print(text, style="#808080")