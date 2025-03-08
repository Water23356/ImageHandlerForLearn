from main import Program
from PyQt5.QtCore import QObject, pyqtSignal, QThread



global program
program:Program = None
global taskThreadRunning
taskThreadRunning = False

def print(message):
    program.cmd.sendMessage(message)
    