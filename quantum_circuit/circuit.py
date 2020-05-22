from .qubit import Qubit
from .register import QuantumRegister
from .utils import Printer

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
    def __init__(self,n,eco_print=False):
        self.n = n
        self.register = QuantumRegister(self.n)
        self.factor = 1
        self.eco_print = eco_print

    def __call__(self,gate,q1,q2=None,phi=None,factor=1.0):
        """
        Apply gate to circuit.

        Input:
            gate   (str)   - Quantum gate to be applied.
            q1     (int)   - Target qubit (if q2 is not it specifies the control qubit.)
            q2     (int)   - (Optional) Target qubit.
            phi    (float) - Rotation angle if gate is rotation gate.
            factor (float) - Factor to be added to gate.
        """
        if q2 != None:
            to_be_appended = get_gate(gate,q1,q2,phi) # in gates.py
            to_be_appended.factor *= factor
        else:
            to_be_appended = gate
            to_be_appended.factor *= factor
        self.register(to_be_appended,q1,q2,phi) # REWRITE

    def __str__(self):
        self.register.update_control_list()
        return Printer().print_circuit(self,eco=self.eco_print)

    def __repr__(self):
        return str(self.factor)+'*'+str(self.register)

    def __eq__(self,other):
        if isinstance(other,QuantumCircuit):
            #self.defactor()
            #other.defactor()
            if self.register == other.register and self.factor == other.factor:
                return True
        return False

    def __add__(self,other):
        assert isinstance(other,QuantumCircuit)==True
        assert self.n == other.n
        assert self.factor == other.factor
        for qbit1,qbit2 in zip(self.register,other.register):
            qbit1.circ += qbit2.circ
        self.register.control_list += other.register.control_list
        return self
                
    def defactor(self):
        self.register.defactor()
        self.factor *= self.register.factor
        self.register.factor = 1

    def copy(self):
        return deepcopy(self)

    def gate_optimization(self):
        self.register.squeeze()

    def remove_identity(self):
        for i in range(self.register.n):
            self.register[i].remove_identity()

    def to_exponent(self):
        paulistring = ''
        qbit_list = []
        factor = self.factor
        for i,qbit in enumerate(self.register):
            assert len(qbit) <= 1 # for now?
            if len(qbit) == 1:
                paulistring += qbit[0].char.upper()
                qbit_list.append(i)
        self.make_empty()
        self.insert_pauli_string([paulistring,qbit_list,factor],exp=True)
        return self

    def make_empty(self):
        self.factor = 1
        self.register = QuantumRegister(self.n)

    def to_qiskit(self,qc=None,qb=None,cb=None):
        if qc == None and qb == None and cb == None:
            qb = qk.QuantumRegister(self.n_qubits)
            cb = qk.ClassicalRegister(self.n_qubits)
            qc = qk.QuantumCircuit(qb,cb)
        
        self.defactor() 
        for i in range(self.n_qubits):
            gate = self.mat[i].circ[j]
            if not isinstance(gate,I):
                qc.append(gate.get_qiskit(),[i],[])
            else:
                ctrl,targ = elem.get_connections()
                qc.append(elem.get_qiskit(),[ctrl,targ],[])
        return qc,qb,cb,self.factor
