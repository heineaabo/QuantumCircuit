from .gate import Gate
from qiskit.extensions.standard import U1Gate,XGate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################

class Ph(Gate):
    """
    Qiskit u1-gate. 
    Not to be confused with actual phase gate.
    """
    def __init__(self,phi,factor=complex(1,0)):
        super().__init__(factor)
        self.phi = phi
        self.char = 'Ph'
    
    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        elif isinstance(other,Ph):
            k = self.factor*other.factor
            return k*I()
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        elif isinstance(other,Zero):
            return Zero()
        else:
            return (self,other)

    def __eq__(self,other):
        if type(self) == type(other):
            if self.phi == other.phi:
                return True
        return False

    def get_qiskit(self):
        return [U1Gate(self.phi),XGate()]


# Hadamard gate to QuantumCircuit functionality
from .. import QuantumCircuit
def ph(self,phi,q):
    self.register.qubits[q].circ.append(Ph(phi))
    self.register.identity_layer(q)
    return self
QuantumCircuit.ph = ph

# Necessary imports
from .identity import I
from .zero import Zero
