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
    def __init__(self,factor=complex(1,0),conv=1):
        """
        conv - Convention for occupation. 
               If occupied orbital is represented as a 0 or a 1.
        """
        super().__init__(factor)
        self.conv = conv

class Creation(Ladder):
    def __init__(self,factor=complex(1,0),conv=1):
        super().__init__(factor,conv)
        self.char = '+'

    def __mul__(self,other):
        if isinstance(other,(Creation,Zero)):
            return Zero()
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        if self.conv: # 1 Convention
            if isinstance(other,Annihilation):
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
            else:
                return (self,other)
        else: # 0 Convention
            if isinstance(other,Annihilation):
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
            else:
                return (self,other)

    def transform(self):
        x = X(factor=0.5*self.factor)
        y = Y(factor=0.5*complex(0,1)*self.factor)
        if self.conv:
            y.factor *= -1
        return [x,y]


class Annihilation(Ladder):
    def __init__(self,factor=complex(1,0),conv=1):
        super().__init__(factor,conv)
        self.char = '-'

    def __mul__(self,other):
        if isinstance(other,(Annihilation,Zero)):
            return Zero()
        elif isinstance(other,I):
            self.factor *= other.factor
            return self
        if self.conv: # 1 Convention
            if isinstance(other,Creation):
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
            else:
                return (self,other)
        else:
            if isinstance(other,Creation):
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
            else:
                return (self,other)
        

    def transform(self):
        x = X(factor=0.5*self.factor)
        y = Y(factor=0.5*complex(0,1)*self.factor)
        if not self.conv:
            y.factor *= -1
        return [x,y]

# Ladder gate to QuantumCircuit functionality
from .. import QuantumCircuit,Qubit #,QuantumRegister
def adg(self,qbit,transf='jw',conv=1):
    """
    Add transformed creation operator to qubit.

    Input:
        qbit (int) - Qubit to apply creation operator.
        transf (str) - Transformation type:
                jw - Jordan-Wigner
                bk - Braviy-Kitaev (TODO)
        conv - Convention for occupied orbital
    """
    if transf.lower() == 'jw':
        for i in range(qbit):
            self.qubits[i].circ.append(Z())
        self.qubits[qbit].circ.append(Creation(conv=conv))
        for j in range(qbit+1,self.n):
            self.qubits[qbit].circ.append(I())
        self.control_list.append(I())
QuantumCircuit.adg = adg

def a(self,qbit,transf='jw',conv=1):
    """
    Add transformed annihilation operator to qubit.

    Input:
        qbit (int) - Qubit to apply annihilation operator.
        transf (str) - Transformation type:
                jw - Jordan-Wigner
                bk - Braviy-Kitaev (TODO)
        conv - Convention for occupied orbital
    """
    if transf.lower() == 'jw':
        for i in range(qbit):
            self.qubits[i].circ.append(Z())
        self.qubits[qbit].circ.append(Annihilation(conv=conv))
        for j in range(qbit+1,self.n):
            self.qubits[qbit].circ.append(I())
        self.control_list.append(I())
QuantumCircuit.a = a


# Necessary imports
from .pauli import X,Y,Z
from .identity import I
from .hadamard import H
from .zero import Zero
