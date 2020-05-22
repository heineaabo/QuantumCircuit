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

# Identity gate to QuantumCircuit functionality
from .. import QuantumCircuit,QuantumRegister
def identity(self,q):
    self.qubits[q].circ.append(I())
    self.identity_layer(q)
    return self
QuantumCircuit.identity = identity

# Register functionality
def identity_layer(self,i,j=None,to_ctrl=True):
    """
    Add layer to circuit -> identity gates on all qubits except i (and j).
    """
    if to_ctrl:
        self.control_list.append(I())
    for k in range(self.n):
        #assert len(self.qubits[k]) in (len(self.control_list),len(self.control_list)-1), '{} not in {}'.format(len(self.qubits[k]),(len(self.control_list),len(self.control_list)-1))
        if k == i or k == j:
            continue
        self.qubits[k].circ.append(I())
    return self
QuantumCircuit.identity_layer = identity_layer

