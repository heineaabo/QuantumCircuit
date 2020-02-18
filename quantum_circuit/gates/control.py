from .gate import Gate

class CTRL(Gate):
    def __init__(self,i):
        super().__init__()
        self.i = i
        self.char = 'C'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            return (self,other)
    
    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            if other.is_identity():
                self.factor *= other.factor
                return self
            else:
                return (self,other)

class TARG(Gate):
    def __init__(self,i,gate):
        super().__init__()
        self.i = i
        self.char = 'T'
        self.gate = gate

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            if other.is_identity():
                self.factor *= other.factor
                return self
            else:
                return (self,other)
    
    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            if other.is_identity():
                self.factor *= other.factor
                return self

# Controlled gates

class CNOT(Gate):
    def __init__(self,ctrl,targ):
        self.c = ctrl # Control qubit
        self.t = targ # Target qubit
        self.char = 'CX'
        self.gate = X()


# QuantumCircuit functionality
from .. import QuantumCircuit
def cx(self,q1,q2):
    c = CTRL(q2)
    t = TARG(q1,X())
    self.register.control_list.append(CNOT(q1,q2))
    self.register[q1].circ.append(c)
    self.register[q2].circ.append(t)
    self.register.identity_layer(q1,q2,to_ctrl=False)
    return self
QuantumCircuit.cx = cx



# Necessary imports
from .pauli import X
