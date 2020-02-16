from .gate import Gate
from .control import CTRL,TARG

class CNOT(Gate):
    def __init__(self,ctrl,targ):
        self.c = ctrl # Control qubit
        self.t = targ # Target qubit
        self.char = 'CX'


