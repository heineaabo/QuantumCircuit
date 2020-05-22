from .gate import Gate
from math import pi
from qiskit.extensions.standard import RXGate,RYGate,RZGate

class Rotation(Gate):
    def __init__(self):
        super().__init__()
        self.phi = 0

    def conj(self):
        self.phi *= -1
        return self

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        elif isinstance(other,Gate):
            if other.is_identity():
                self.factor *= other.factor
                return self
            if type(self) == type(other):
                if self.phi == -other.phi:
                    return I(factor=self.factor*other.factor)
                elif self.phi == other.phi:
                    factor = -complex(0,1)*self.factor*other.factor
                    if isinstance(self,Rx):
                        new_gate = X(factor=factor)
                    if isinstance(self,Ry):
                        new_gate = Y(factor=factor)
                    if isinstance(self,Rz):
                        new_gate = Z(factor=factor)
                    return new_gate
        return (self,other)

    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        elif isinstance(other,Gate):
            if other.is_identity():
                self.factor *= other.factor
                return self
            if type(self) == type(other):
                if self.phi == -other.phi:
                    return I(factor=self.factor*other.factor)
                elif self.phi == other.phi:
                    factor = -complex(0,1)*self.factor*other.factor
                    if isinstance(self,Rx):
                        new_gate = X(factor=factor)
                    if isinstance(self,Ry):
                        new_gate = Y(factor=factor)
                    if isinstance(self,Rz):
                        new_gate = Z(factor=factor)
                    return new_gate
                    
        return (other,self)

    def __eq__(self,other):
        if isinstance(other,Rotation):
            if type(self) == type(other)\
                    and self.factor == other.factor\
                    and self.phi == other.phi:
                return True
            else:
                return False
        else:
            return False


class Rx(Rotation):
    def __init__(self,phi=pi/2):
        super().__init__()
        self.phi = phi
        self.char = 'Rx'

    def get_qiskit(self):
        return RXGate(self.phi)
        
class Ry(Rotation):
    def __init__(self,phi=pi/2):
        super().__init__()
        self.phi = phi
        self.char = 'Ry'

    def get_qiskit(self):
        return RYGate(self.phi)
        
class Rz(Rotation):
    def __init__(self,phi=pi/2):
        super().__init__()
        self.phi = phi
        self.char = 'Rz'

    def get_qiskit(self):
        return RZGate(self.phi)
        

from .. import QuantumCircuit
def rx(self,q,phi=pi/2):
    self.qubits[q].apply(Rx(phi=phi))
    self.identity_layer(q)
    return self
QuantumCircuit.rx = rx

def ry(self,q,phi=pi/2):
    self.qubits[q].apply(Ry(phi=phi))
    self.identity_layer(q)
    return self
QuantumCircuit.ry = ry

def rz(self,q,phi=pi/2):
    self.qubits[q].apply(Rz(phi=phi))
    self.identity_layer(q)
    return self
QuantumCircuit.rz = rz

# Necessary import
from .identity import I
