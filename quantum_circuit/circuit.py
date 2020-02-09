from .qubit import Qubit
from .register import QuantumRegister
from .utils import Printer,get_permutations

from math import pi
from copy import deepcopy

class QuantumCircuit:
    """
    Quantum Circuit class.
    Handles gate action and stores QuantumRegister class.

    Input:
        n (int) - Number of qubits.

    Attributes:
        register (QuantumRegister) - Handles all qubit action.
    """
    def __init__(self,n):
        self.register = QuantumRegister(n)
        self.factor = 1

    def __call__(self,gate,q1,q2=None,phi=None,factor=1.0):
        """
        Apply gate to circuit.

        Input:
            gate   (str)   - Quantum gate to be applied.
            q1     (int)   - Target qubit (if q2 is not it specifies the control qubit.)
            q2     (int)   - (Optional) Target qubit.
            phi    (float) - Roation angle if gate is rotation gate.
            factor (float) - Factor to be added to gate.
        """
        if q2 != None:
            to_be_apended = get_gate(gate,q1,q2,phi,factor) # in gates.py
        else:
            to_be_appended = gate
        self.register[q1].append(to_be_appended)

    def __str__(self):
        return Printer().print_circuit(self)

    def copy(self):
        return deepcopy(self)

    def gate_optimization(self):
        self.register.optimize()

    def optimize(self):
        self.check_ladder()
    
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
                circ.register[qbit].circ[ind] = gate
        return copies
        
    def insert_one_body_operator(self,h,i,a):
        """
        Insert one-body second quantized operator on form:
            <i|h|a> a_a^\dagger a_i

        Input:
            i (int)   - Orbital to annihilate
            a (int)   - Orbital to create
            h (float) - Matrix element
        """
        self.register.add_annihilation(i)
        self.register.add_creation(a)
        self.factor *= h

    def insert_two_body_operator(self,v,i,j,a,b):
        """
        Insert two-body second quantized operator on form:
            <ij|v|ab> a_a^\dagger a_b^\dagger a_j a_i

        Input:
            i (int)   - Orbital to annihilate
            j (int)   - Orbital to annihilate
            a (int)   - Orbital to create
            b (int)   - Orbital to create
            v (float) - Matrix element
        """
        self.register.add_annihilation(i)
        self.register.add_annihilation(j)
        self.register.add_creation(b)
        self.register.add_creation(a)
        self.factor *= v

    def to_qiskit(self,qc=None,qb=None,cb=None):
        if qc == None and qb == None and cb == None:
            qb = qk.QuantumRegister(self.n_qubits)
            cb = qk.ClassicalRegister(self.n_qubits)
            qc = qk.QuantumCircuit(qb,cb)
        
        for i in range(self.n_qubits):
            gate = self.mat[i].circ[j]
            if not isinstance(gate,I):
                qc.append(gate.get_qiskit(),[i],[])
            else:
                ctrl,targ = elem.get_connections()
                qc.append(elem.get_qiskit(),[ctrl,targ],[])
        return qc,qb,cb
