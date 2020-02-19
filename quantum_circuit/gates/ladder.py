from .gate import Gate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################

class Ladder(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)

class Creation(Ladder):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = '+'

    def __mul__(self,other):
        if isinstance(other,Creation):
            return Zero()
        elif isinstance(other,Annihilation):
            k = self.factor*other.factor
            Id = (0.5*k)*I()
            z = (0.5*k)*Z()
            return [Id,z]
        elif isinstance(other,X):
            k = self.factor*other.factor
            Id = (0.5*k)*I()
            z = (0.5*k)*Z()
            return [Id,z]
        elif isinstance(other,Y):
            i = complex(0,1)
            k = self.factor*other.factor
            Id = (-0.5*i*k)*I()
            z = (-0.5*i*k)*Z()
            return [Id,z]
        elif isinstance(other,Z):
            self.factor *= other.factor
            self.factor *= -1
            return self
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        elif isinstance(other,Zero):
            return Zero()
        elif isinstance(other,H):
            return (self,other)
        #elif isinstance(other,):

    def transform(self):
        x = X(factor=0.5*self.factor)
        y = Y(factor=-0.5*complex(0,1)*self.factor)
        return [x,y]


class Annihilation(Ladder):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = '-'

    def __mul__(self,other):
        if isinstance(other,Annihilation):
            return Zero()
        elif isinstance(other,Creation):
            k = self.factor*other.factor
            Id = (0.5*k)*I()
            z = (-0.5*k)*Z()
            return [Id,z]
        elif isinstance(other,X):
            k = self.factor*other.factor
            Id = (0.5*k)*I()
            z = (-0.5*k)*Z()
            return [Id,z]
        elif isinstance(other,Y):
            i = complex(0,1)
            k = self.factor*other.factor
            Id = (0.5*i*k)*I()
            z = (-0.5*i*k)*Z()
            return [Id,z]
        elif isinstance(other,Z):
            self.factor *= other.factor
            return self
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        elif isinstance(other,Zero):
            return Zero()
        elif isinstance(other,H):
            return (self,other)

    def transform(self):
        x = X(factor=0.5*self.factor)
        y = Y(factor=0.5*complex(0,1)*self.factor)
        return [x,y]

# Ladder gate to QuantumCircuit functionality
from .. import QuantumCircuit,QuantumRegister,Qubit
def adg(self,qbit,transf='jw'):
    """
    Add transformed creation operator to qubit.

    Input:
        qbit (int) - Qubit to apply creation operator.
        transf (str) - Transformation type:
                jw - Jordan-Wigner
                bk - Braviy-Kitaev (TODO)
    """
    if transf.lower() == 'jw':
        for i in range(qbit):
            self.register.qubits[i].circ.append(Z())
        self.register.qubits[qbit].circ.append(Creation())
        for j in range(qbit+1,self.register.n):
            self.register.qubits[qbit].circ.append(I())
        self.register.control_list.append(I())
QuantumCircuit.adg = adg

def a(self,qbit,transf='jw'):
    """
    Add transformed annihilation operator to qubit.

    Input:
        qbit (int) - Qubit to apply annihilation operator.
        transf (str) - Transformation type:
                jw - Jordan-Wigner
                bk - Braviy-Kitaev (TODO)
    """
    if transf.lower() == 'jw':
        for i in range(qbit):
            self.register.qubits[i].circ.append(Z())
        self.register.qubits[qbit].circ.append(Annihilation())
        for j in range(qbit+1,self.register.n):
            self.register.qubits[qbit].circ.append(I())
        self.register.control_list.append(I())
QuantumCircuit.a = a


# Necessary imports
from .pauli import X,Y,Z
from .identity import I
from .hadamard import H
from .zero import Zero
