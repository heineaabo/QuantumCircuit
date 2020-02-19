from .gate import Gate
from math import pi

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
        if isinstance(other,Gate):
            return (self,other)
        return (self,other)

    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        #if isinstance(other,Gate):
        #    return (other,self)
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
        
class Ry(Rotation):
    def __init__(self,phi=pi/2):
        super().__init__()
        self.phi = phi
        self.char = 'Ry'

class Rz(Rotation):
    def __init__(self,phi=pi/2):
        super().__init__()
        self.phi = phi
        self.char = 'Rz'


from .. import QuantumCircuit
def rx(self,q,phi=pi/2):
    self.register.qubits[q].apply(Rx(phi=phi))
    self.register.identity_layer(q)
    return self
QuantumCircuit.rx = rx

def ry(self,q,phi=pi/2):
    self.register.qubits[q].apply(Ry(phi=phi))
    self.register.identity_layer(q)
    return self
QuantumCircuit.ry = ry

def rz(self,q,phi=pi/2):
    self.register.qubits[q].apply(Rz(phi=phi))
    self.register.identity_layer(q)
    return self
QuantumCircuit.rz = rz
