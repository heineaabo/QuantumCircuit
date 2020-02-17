from .gate import Gate
from .pauli import X,Y,Z
from .identity import I
from .hadamard import H
from .ladder import Creation,Annihilation
from .zero import Zero
import sys
sys.path.append('..')
from .. import QuantumCircuit,QuantumRegister,Qubit


def get_gate(gate,q1,q2,phi):
    """
    Prepare control gate.

    Input:
        gate (str)  : Quantum gate, string representation.
        q1   (int)  : Control qubit (or main qubit if single gate)
        q2   (int)  : Target qubit.
        phi  (float): Rotation angle if rotation gate.
    """
    pass


# Identity gate to QuantumCircuit functionality
def identity(self,q):
    self.register.qubits[q].append(I())
    self.register.identity_layer(q)
    return self
QuantumCircuit.identity = identity

# Hadamard gate to QuantumCircuit functionality
def h(self,q):
    self.register.qubits[q].append(H())
    self.register.identity_layer(q)
    return self
QuantumCircuit.h = h

# Pauli gate to QuantumCircuit functionality
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
QuantumCircuit.y = z

    

# Ladder gate to QuantumCircuit functionality
def adagger(self,q):
    """Creation operator"""
    self.register.qubits[q].apply(Creation())
    self.register.identity_layer(q)
    return self

def a(self,q):
    """Annihilation operator"""
    self.register.qubits[q].apply(Creation())
    self.register.identity_layer(q)
    return self

def transform_ladder_operators(self):
    self.gate_optimization()
    info = self.register.check_ladder()
    num = 0 # Number of new 
    each_ladder = []
    for elem in info:
        i = elem[0]
        for j in elem[1]:
            num += 1
            each_ladder.append([i,j])
    copies = [self.copy() for i in range(2**num)]
    perms = get_permutations(num)
    assert len(copies) == len(perms)
    for perm,circ in zip(perms,copies):
        for j,gate in enumerate(perm):
            qbit,ind = each_ladder[j]
            gate.factor *= circ.register[qbit].circ[ind].factor
            if isinstance(circ.register[qbit].circ[ind],Creation)\
                    and isinstance(gate,Y):
                gate.factor *= -1
            circ.register[qbit].circ[ind] = gate
    for circ in copies:
        circ.gate_optimization()
        circ.defactor()
    unique = [copies[0]]
    for circ1 in copies[1:]:
        check = False
        for circ2 in unique:
            if circ1.register == circ2.register:
                circ2.factor += circ1.factor
                check = True
                break
        if not check:
            unique.append(circ1)
    return unique

QuantumCircuit.adagger = adagger
QuantumCircuit.a = a
QuantumCircuit.transform_ladder_operators = transform_ladder_operators



# Qubit functionality
def get_all_ladder(self):
    """
    Returns position of all ladder operations on qubit.
    """
    num_ladder = 0
    ladder_operators = []
    for i,gate in enumerate(self.circ):
        if isinstance(gate,(Creation,Annihilation)):
            ladder_operators.append(i)
        else:
            continue
    return ladder_operators
Qubit.get_all_ladder = get_all_ladder

def is_empty(self):
    check = True
    for gate in self.circ:
        if not isinstance(gate,I):
            check = False
    return check
Qubit.is_empty = is_empty


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

def add_creation(self,qbit,transf='jw'):
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
            self(Z(),i)
        self(Creation(),qbit)
QuantumRegister.add_creation = add_creation

def add_annihilation(self,qbit,transf='jw'):
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
            self(Z(),i)
        self(Creation(),qbit)
QuantumRegister.add_annihilation = add_annihilation
