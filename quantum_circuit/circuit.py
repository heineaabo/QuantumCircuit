from .qubit import Qubit
from .register import QuantumRegister
from .utils import Printer#,get_permutations
#from .gates import Creation,Y, get_gate

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
        self.register = QuantumRegister(n)
        self.factor = 1
        self.eco_print = eco_print

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
            to_be_appended = get_gate(gate,q1,q2,phi) # in gates.py
            to_be_appended.factor *= factor
        else:
            to_be_appended = gate
            to_be_appended.factor *= factor
        self.register(to_be_appended,q1,q2,phi) # REWRITE

    def __str__(self):
        return Printer().print_circuit(self,eco=eco_print)

    def __eq__(self,other):
        if isinstance(other,QuantumCircuit):
            self.defactor()
            other.defactor()
            #if self.factor == other.factor:
            #    print('factor equal',self.factor,other.factor)
            #else:
            #    print('factor Not equal',self.factor,other.factor)
            #if self.register == other.register:
            #    print('register equal',self.register,other.register)
            #else:
            #    print('register Not equal',self.register,other.register)
            if self.register == other.register and self.factor == other.factor:
                return True
        return False
                
    def defactor(self):
        self.register.defactor()
        self.factor *= self.register.factor
        self.register.factor = 1

    def copy(self):
        return deepcopy(self)

    def gate_optimization(self):
        self.register.optimize()

    def remove_identity(self):
        for i in range(self.register.n):
            self.register[i].remove_identity()

    #def transform_ladder_operators(self):
    #    self.gate_optimization()
    #    info = self.register.check_ladder()
    #    num = 0 # Number of new 
    #    each_ladder = []
    #    for elem in info:
    #        i = elem[0]
    #        for j in elem[1]:
    #            num += 1
    #            each_ladder.append([i,j])
    #    copies = [self.copy() for i in range(2**num)]
    #    perms = get_permutations(num)
    #    assert len(copies) == len(perms)
    #    for perm,circ in zip(perms,copies):
    #        for j,gate in enumerate(perm):
    #            qbit,ind = each_ladder[j]
    #            gate.factor *= circ.register[qbit].circ[ind].factor
    #            if isinstance(circ.register[qbit].circ[ind],Creation)\
    #                    and isinstance(gate,Y):
    #                gate.factor *= -1
    #            circ.register[qbit].circ[ind] = gate
    #    for circ in copies:
    #        circ.gate_optimization()
    #        circ.defactor()
    #    unique = [copies[0]]
    #    for circ1 in copies[1:]:
    #        check = False
    #        for circ2 in unique:
    #            if circ1.register == circ2.register:
    #                circ2.factor += circ1.factor
    #                check = True
    #                break
    #        if not check:
    #            unique.append(circ1)
    #    return unique
        
    def insert_one_body_operator(self,h,i,a):
        """
        Insert one-body second quantized operator on form:
            ⟨a∣h∣i⟩ a_a^\dagger a_i

        Input:
            i (int)   - Orbital to annihilate
            a (int)   - Orbital to create
            h (float) - Matrix element
        """
        self.a(i)
        self.adg(a)
        self.factor *= h

    def insert_two_body_operator(self,v,i,j,a,b):
        """
        Insert two-body second quantized operator on form:
            ⟨ab∣h∣ij⟩ a_a^\dagger a_b^\dagger a_j a_i

        Input:
            i (int)   - Orbital to annihilate
            j (int)   - Orbital to annihilate
            a (int)   - Orbital to create
            b (int)   - Orbital to create
            v (float) - Matrix element
        """
        self.a(i)
        self.a(j)
        self.adg(b)
        self.adg(a)
        self.factor *= v

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

    def compare_to_control(self):
        """
        Move all gates with respect to control operations and insert identity
        gates to isolate "regions" of single qubit gates between control gates.
        Probably only necessary for printing.
        """
        pass
