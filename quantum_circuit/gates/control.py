from .gate import Gate
from qiskit.extensions.standard import CnotGate

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
            if other.is_identity():
                self.factor *= other.factor
                return self
        return (self,other)
    
    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            if other.is_identity():
                self.factor *= other.factor
                return self
        return (other,self)

    def __eq__(self,other):
        if isinstance(other,CTRL):
            if self.factor == other.factor\
                    and self.i == other.i:
                return True
            else:
                return False
        else:
            return False

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
        elif isinstance(other,Rotation):
            return (self,other)
    
    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            if other.is_identity():
                self.factor *= other.factor
                return self
        elif isinstance(other,Rotation):
            return (other,self)

    def __eq__(self,other):
        if isinstance(other,TARG):
            if self.factor == other.factor\
                    and self.i == other.i\
                    and self.gate == other.gate:
                return True
            else:
                return False
        else:
            return False

# Controlled gates

class ControlGate(Gate):
    def __init__(self):
        super().__init__()
        self.ctrl = None
        self.targ = None
        self.gate = None

    def __eq__(self,other):
        if isinstance(other,ControlGate):
            if self.factor == other.factor\
                    and self.c == other.c\
                    and self.t == other.t\
                    and self.gate == other.gate:
                return True
            else:
                return False
        else:
            return False


class CNOT(ControlGate):
    def __init__(self,ctrl,targ):
        super().__init__()
        self.c = ctrl # Control qubit
        self.t = targ # Target qubit
        self.char = 'CX'
        self.gate = X()

    def get_qiskit(self):
        return CnotGate()

class C(ControlGate):
    def __init__(self,gate,ctrl,targ):
        super().__init__()
        self.c = ctrl # Control qubit
        self.t = targ # Target qubit
        self.char = 'C'+gate.char
        self.gate = gate


# QuantumCircuit functionality
from .. import QuantumCircuit
def cx(self,q1,q2):
    c = CTRL(q2)
    t = TARG(q1,X())
    self.control_list.append(CNOT(q1,q2))
    self[q1].circ.append(c)
    self[q2].circ.append(t)
    self.identity_layer(q1,q2,to_ctrl=False)
    return self
QuantumCircuit.cx = cx

def cy(self,q1,q2):
    c = CTRL(q2)
    t = TARG(q1,Y())
    self.control_list.append(C(Y(),q1,q2))
    self[q1].circ.append(c)
    self[q2].circ.append(t)
    self.identity_layer(q1,q2,to_ctrl=False)
    return self
QuantumCircuit.cy = cy

def cz(self,q1,q2):
    c = CTRL(q2)
    t = TARG(q1,Z())
    self.control_list.append(C(Z(),q1,q2))
    self[q1].circ.append(c)
    self[q2].circ.append(t)
    self.identity_layer(q1,q2,to_ctrl=False)
    return self
QuantumCircuit.cz = cz


# Necessary imports
from .pauli import X,Y,Z
from .rotation import Rotation
