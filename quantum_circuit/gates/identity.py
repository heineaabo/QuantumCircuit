from .gate import Gate
from qiskit.extensions.standard import IdGate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################

class I(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'I'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            other.factor *= self.factor
            return other

    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            other.factor *= self.factor
            return other
