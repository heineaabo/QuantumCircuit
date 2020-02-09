from .gate import Gate
from qiskit.extensions.standard import HGate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################

class H(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'H'
    
    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            if isinstance(other,I):
                self.factor *= other.factor
                return self
            else:
                return (self,other)
        else:
            raise ValueError('Can not multiply instance {} with instance {}'.format(type(self),type(other)))

    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            if isinstance(other,I):
                self.factor *= other.factor
                return self
            else:
                return (other,self)
        else:
            raise ValueError('Can not multiply instance {} with instance {}'.format(type(self),type(other)))

    def get_qiskit(self):
        return HGate()


