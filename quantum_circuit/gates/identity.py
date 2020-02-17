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

    #def __rmul__(self,other):
    #    if isinstance(other,(int,float,complex)):
    #        self.factor *= other
    #        return self
    #    if isinstance(other,Gate):
    #        other.factor *= self.factor
    #        return other

# Identity gate to QuantumCircuit functionality
from .. import QuantumCircuit,QuantumRegister
def identity(self,q):
    self.register.qubits[q].append(I())
    self.register.identity_layer(q)
    return self
QuantumCircuit.identity = identity

# Register functionality
def identity_layer(self,i,to_ctrl=True):
    """
    Add layer to circuit -> identity gates on all qubits except i.
    """
    self.controls.append(I())
    for j,q in enumerate(self.qubits):
        if j != i:
            q.apply(I())
QuantumRegister.identity_layer = identity_layer

