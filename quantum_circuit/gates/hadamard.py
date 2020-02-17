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
        elif isinstance(other,H):
            k = self.factor*other.factor
            return k*I()
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        elif isinstance(other,X):
            return (self,other)
        elif isinstance(other,Y):
            return (self,other)
        elif isinstance(other,Z):
            return (self,other)
        elif isinstance(other,Creation):
            return (self,other)
        elif isinstance(other,Annihilation):
            return (self,other)
        elif isinstance(other,Zero):
            return Zero()

    def get_qiskit(self):
        return HGate()


# Hadamard gate to QuantumCircuit functionality
from .. import QuantumCircuit
def h(self,q):
    self.register.qubits[q].append(H())
    self.register.identity_layer(q)
    return self
QuantumCircuit.h = h

# Necessary imports
from .identity import I
from .zero import Zero
from .ladder import Creation,Annihilation
from .pauli import X,Y,Z
