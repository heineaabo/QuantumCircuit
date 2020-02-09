from .gate import Gate
from qiskit.extensions.standard import YGate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################

class Y(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'Y'

    def __mul__(self,other):
        i = complex(0,1)
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,I):
            self.factor *= other.factor
            return self
        if isinstance(other, X):
            new = Z(factor=self.factor*other.factor)
            return i*new
        if isinstance(other, Z):
            new = X(factor=self.factor*other.factor)
            return -i*new
        if isinstance(other,H):
            return (self,other)
        if type(self) == type(other):
            new = I(factor=self.factor*other.factor)
            return new

    def get_qiskit(self):
        return YGate()

