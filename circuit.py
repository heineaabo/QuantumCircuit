import numpy as np
import qiskit as qk

from gates import *
from qubit import *
from optimizer import *
from jordan_wigner import simple_remove_z
from copy import deepcopy

class QuantumCircuit:
    def __init__(self,n):
        self.n_qubits = n
        self.mat = [Qubit(name=str(i)) for i in range(n)]
        self.control_circuit = []
        self.min_ctrl = 0 #Position of last controlled operation
        self.factor = 1

    def apply(self,O,i=None,pos=None):
        """
        Apply gate O (to qubit i if O is not a control gate).
        """
        if isinstance(O,OneQubitGate):
            self.add_gate(O,i,pos)
        if isinstance(O,ControlGate):
            if pos == None:
                ctrl,targ = O.get_connections()
                for j in range(self.n_qubits):
                    self.mat[j].Identity()
                self.mat[ctrl].circ[-1] = CTRL(targ)
                self.mat[targ].circ[-1] = TARG(ctrl,O.gate)
                self.control_circuit.append(O) 
                self.min_ctrl = len(self.control_circuit)
            else:
                ctrl,targ = O.get_connections()
                for j in range(self.n_qubits):
                    self.mat[j].Identity()
                self.mat[ctrl].circ.insert(pos,(CTRL(targ)))
                self.mat[ctrl].circ.insert(pos,(TARG(ctrl,O.gate)))
                self.control_circuit.insert(pos,O) 
                if pos > slef.min_ctrl:
                    self.min_ctrl = pos


    def add_gate(self,O,i,pos=None):
        """
        Add gate O to qubit i in circuit. 
        Add identity gate to all other qubits.
        Add identity to control_circuit.
        """
        assert len(self.control_circuit) == len(self.mat[0].circ)
        if pos == None:
            if self.mat[i].act(O,self.min_ctrl):
                for j in range(self.n_qubits):
                    if j != i:
                        self.mat[j].Identity()
                self.control_circuit.append(Id())
        else:
            self.mat[i].circ.insert(pos,O)
            for j in range(self.n_qubits):
                if j != i:
                    self.mat[j].circ.insert(pos,Id())
            self.control_circuit.insert(pos,Id())

    
    def add_creation(self,l):
        """
        Add Jordan-Wigner transformed creation operator to qubit l.
        """
        n = self.n_qubits
        assert l < n
        if l > 0:
            for i in range(l):
                self.add_gate(Z(),i)
        self.add_gate(Create(),l)

    def add_annihilation(self,l):
        """
        Add Jordan-Wigner transformed annihilation operator to qubit l.
        """
        n = self.n_qubits
        assert l < n
        if l > 0:
            for i in range(l):
                self.add_gate(Z(),i)
        self.add_gate(Annihilate(),l)

    def optimize(self,jw=False):
        """
        input jw (bool) - If to add simple z removal for jw- transformation
        """
        self = Optimizer(self).run()
        if jw:
            for i in range(self.n_qubits):
                self.mat[i] = simple_remove_z(self.mat[i])
                
    def check_all_identity(self,d):
        check = True
        for i in range(self.n_qubits):
            if not isinstance(self.mat[i][d],Id):
                check = False
        return check

    def check_ladder(self):
        check = False
        for i in range(self.n_qubits):
            for j in range(len(self.mat[i].circ)):
                if isinstance(self.mat[i].circ[j],(Create,Annihilate)):
                    check = True
        return check

    def transform_ladder(self):
        """
        Transform first occuring ladder operator, if present, in circuit.
        Returns new circuit with Y operator in place of ladder operator.
        In addition, changes itself to X operator in place of ladder operator
        TODO:
            Change so it transforms all ladder operators in one call.
        """
        break_bool = False # To break out of first loop
        for i in range(self.n_qubits):
            for j in range(len(self.mat[i].circ)):
                if isinstance(self.mat[i].circ[j],Create):
                    new_circ = self.copy()
                    self.mat[i].circ[j] = X()
                    new_circ.mat[i].circ[j] = Y()
                    new_circ.factor = np.complex(0,1)
                    break_bool = True
                    break
                elif isinstance(self.mat[i].circ[j],Annihilate):
                    new_circ = self.copy()
                    self.mat[i].circ[j] = X()
                    new_circ.mat[i].circ[j] = Y()
                    new_circ.factor = -np.complex(0,1)
                    break_bool = True
                    break
            if break_bool:
                break
        return new_circ

    def transform_to_pauli_z(self,exponent=False):
        if not exponent:
            for i in range(self.n_qubits):
                for j in range(len(self.mat[i].circ)):
                    gate = self.mat[i].circ[j]
                    if isinstance(gate,X):
                        self.mat[i].circ[j] = Z()
                        self.apply(H(),i=i,pos=j+1)
                        self.apply(H(),i=i,pos=j)
                    elif isinstance(gate,Y):
                        self.mat[i].circ[j] = Z()
                        self.apply(H(),i=i,pos=j+1)
                        self.apply(Rx(),i=i,pos=j+1)
                        self.apply(Rx(),i=i,pos=j)
                        self.apply(H(),i=i,pos=j)
                    elif isinstance(gate,Z):
                        continue

    def insert_pauli_string(self,string,exp=False,coefficient=1):
        """
        Assume pauli string on form {operations}_{qubits}.
        Example:
                XXYX_1345
                    - X() on qubit 1
                    - X() on qubit 3
                    - Y() on qubit 4
                    - X() on qubit 5
        """
        operations,qubits = string.split('_')
        qubits = [int(i) for i in qubits]
        if exp:
            for i,o in zip(qubits,operations):
                if o.upper() == 'X':
                    self.apply(H(),i)
                elif o.upper() == 'Y':
                    self.apply(H(),i)
                    self.apply(Rx(),i)
            for i in qubits[:-1]:
                self.apply(ControlGate(X(),i,qubits[-1]))
            self.apply(Rz(phi=coefficient),qubits[-1])
            for i in reversed(qubits[:-1]):
                self.apply(ControlGate(X(),i,qubits[-1]))
            for i,o in zip(qubits,operations):
                if o.upper() == 'X':
                    self.apply(H(),i)
                elif o.upper() == 'Y':
                    self.apply(Rx().dagger(),i)
                    self.apply(H(),i)
        else:
            for i,o in zip(qubits):
                if o.upper() == 'X':
                    self.apply(H(),i)
                    self.apply(Z(),i)
                    self.apply(H(),i)
                elif o.upper() == 'Y':
                    self.apply(H(),i)
                    self.apply(Rx(),i)
                    self.apply(Z(),i)
                    self.apply(Rx(),i)
                    self.apply(H(),i)







    def copy(self):
        return deepcopy(self)

    def to_qiskit(self,qc=None,qb=None,cb=None):
        if qc == None and qb == None and cb == None:
            qb = qk.QuantumRegister(self.n_qubits)
            cb = qk.ClassicalRegister(self.n_qubits)
            qc = qk.QuantumCircuit(qb,cb)
        
        for j,elem in enumerate(self.control_circuit):
            if isinstance(elem,Id):
                for i in range(self.n_qubits):
                    gate = self.mat[i].circ[j]
                    if not isinstance(gate,Id):
                        qc.append(gate.get_qiskit(),[i],[])
            else:
                ctrl,targ = elem.get_connections()
                qc.append(elem.get_qiskit(),[ctrl,targ],[])
        return qc,qb,cb

    def __add__(self,other):
        """
        Combine two qunatum circuits.
        """
        if isinstance(other,QuantumCircuit):
            if self.n_qubits == other.n_qubits:
                for i in range(self.n_qubits):
                    self.mat[i] += other.mat[i]
                self.min_ctrl = len(self.control_circuit) + other.min_ctrl
                self.control_circuit += other.control_circuit
                self.factor *= other.factor
                
                return self
        

    def __repr__(self):
        return str(self.mat)

    def __str__(self):
        string = 'Circuit:\n'
        for i,qbit in enumerate(self.mat):
            string += qbit.print_gates(self.control_circuit,i) + '\n'
        return string

    def __eq__(self,other):
        if repr(self) == repr(other):
            return self.factor == other.factor
        else:
            return False
        #if isinstance(other,QuantumCircuit):
        #    if other.n_qubits == self.n_qubits and self.factor == other.factor\
        #    and len(self.control_circuit) == len(other.control_circuit):
        #        check = True
        #        for i in range(self.n_qubits):
        #            for j in range(len(self.mat[i].circ)):
        #                if type(self.mat[i].circ[j]) == type(other.mat[i].circ[j]):
        #                    continue
        #                else:
        #                    check == False
        #        return check
        #    else:
        #        return False 
        #else:
        #    return False

    def __mul__(self,other):
        self.factor *= other
        return self

    def __rmul__(self,other):
        self.factor *= other
        return self

    def __neg__(self):
        cp = self.copy()
        cp.factor = -self.factor
        return cp

