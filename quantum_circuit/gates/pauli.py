from .gate import Gate
from qiskit.extensions.standard import XGate,YGate,ZGate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################

class Pauli(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)

class X(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'X'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        elif type(self) == type(other):
            k = self.factor*other.factor
            return k*I()
        elif isinstance(other,Y):
            i = complex(0,1)
            k = self.factor*other.factor
            return -i*k*Z()
        elif isinstance(other,Z):
            i = complex(0,1)
            k = self.factor*other.factor
            return i*k*Y()
        elif isinstance(other,Ladder):
            k = self.factor*other.factor
            Id = 0.5*k*I() 
            z = 0.5*k*Z()
            if (isinstance(other,Creation) and other.conv == 1)\
                    or (isinstance(other,Annihilation) and other.conv == 0):
                z.factor *= -1
            return [Id,z]
        elif isinstance(other,Zero):
            return Zero()
        else:
            return (self,other)
    
    def get_qiskit(self):
        return XGate()

class Y(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'Y'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        elif type(self) == type(other):
            k = self.factor*other.factor
            return k*I()
        elif isinstance(other,X):
            i = complex(0,1)
            k = self.factor*other.factor
            return i*k*Z()
        elif isinstance(other,Z):
            i = complex(0,1)
            k = self.factor*other.factor
            return -i*k*X()
        elif isinstance(other,Ladder):
            i = complex(0,1)
            k = self.factor*other.factor
            Id = 0.5*i*k*I() 
            z = 0.5*i*k*Z()
            if (isinstance(other,Creation) and other.conv == 1)\
                    or (isinstance(other,Annihilation) and other.conv == 0):
                Id.factor *= -1
            return [Id,z]
        elif isinstance(other,Zero):
            return Zero()
        else:
            return (self,other)

    def get_qiskit(self):
        return YGate()

class Z(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'Z'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        elif type(self) == type(other):
            k = self.factor*other.factor
            return k*I()
        elif isinstance(other,X):
            i = complex(0,1)
            k = self.factor * other.factor
            return -i*k*Y()
        elif isinstance(other,Y):
            i = complex(0,1)
            k = self.factor * other.factor
            return i*k*X()
        elif isinstance(other,Ladder):
            other.factor *= self.factor
            if (isinstance(other,Creation) and other.conv == 0)\
                    or (isinstance(other,Annihilation) and other.conv == 1):
                other.factor *= -1
            return other
        elif isinstance(other,Zero):
            return Zero()
        else:
            return (self,other)

    def get_qiskit(self):
        return ZGate()


# Pauli gate to QuantumCircuit functionality
from .. import QuantumCircuit
def x(self,q):
    self.register.qubits[q].apply(X())
    self.register.identity_layer(q)
    return self
def y(self,q):
    self.register.qubits[q].apply(Y())
    self.register.identity_layer(q)
    return self
def z(self,q):
    self.register.qubits[q].apply(Z())
    self.register.identity_layer(q)
    return self

QuantumCircuit.x = x
QuantumCircuit.y = y
QuantumCircuit.z = z


# Necessary import
from .ladder import Creation,Annihilation,Ladder
from .identity import I
from .zero import Zero
