from .qubit import Qubit
#from .register import QuantumRegister
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
        #self.register = QuantumRegister(self.n)
        self.qubits = [Qubit(name=str(i)) for i in range(n)]
        self.control_list = []
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
            gate = get_gate(gate,q1,q2,phi) # in gates.py
            gate.factor *= factor
        else:
            gate.factor *= factor
            self.qubits[q1].apply(gate,q1,phi=phi)
            self.identity_layer(q1)

    def __str__(self):
        self.register.update_control_list()
        return Printer().print_circuit(self,eco=self.eco_print)

    def __repr__(self):
        if self.factor == 1:
            return str(self.qubits)
        return str(self.factor)+'*'+str(self.qubits)

    def __eq__(self,other):
        if isinstance(other,QuantumCircuit):
            if self.n == other.n: # Same amount of qubits
                self.defactor()
                other.defactor()
                if self.factor == other.factor:
                    for i in range(self.n):
                        if self.qubits[i] != other.qubits[i]:
                            return False
                    return True
        return False

    def equal_to(self,other):
        """
        Check if two circuits are equal, ignore factor.
        """
        if isinstance(other,QuantumCircuit):
            if self.n == other.n: # Same amount of qubits
                #self.defactor()
                #other.defactor()
                for i in range(self.n):
                    if self.qubits[i] != other.qubits[i]:
                        return False
                return True
        return False


    def __add__(self,other):
        assert isinstance(other,QuantumCircuit)==True
        assert self.n == other.n
        assert self.factor == other.factor
        for qbit1,qbit2 in zip(self.qubits,other.qubits):
            qbit1.circ += qbit2.circ
        self.control_list += other.control_list
        return self

    def __len__(self):
        return len(self.qubits)

    def __iter__(self):
        return iter(self.qubits)

    def __getitem__(self,i):
        if i > self.n:
            raise ValueError('Qubit {} not available in register with {} qubits.'.format(i,self.n))
        return self.qubits[i]
                
    def defactor(self):
        """
        Defactor all qubits to self.factor.
        """
        for i in range(self.n):
            # Defactor qubit
            self[i].defactor() 
            # Add to circuit factor
            self.factor *= self[i].factor
            self[i].factor = 1

    def append(self,qbit,check_name=True):
        """
        Append a qbit to register.

        Input:
            qbit (Qubit)      - Qubit to be appended
            check_name (bool) - Changes Qubit.name to its 
                                position in register.
        """
        if check_name:
            qbit.name = str(self.n)    
        self.qubits.append(qbit)
        self.n += 1

    def copy(self):
        return deepcopy(self)

    def gate_optimization(self):
        self.squeeze()

    def remove_identity(self):
        for i in range(self.n):
            self[i].remove_identity()

    def to_exponent(self):
        paulistring = ''
        qbit_list = []
        factor = self.factor
        for i,qbit in enumerate(self.qubits):
            assert len(qbit) <= 1 # for now?
            if len(qbit) == 1:
                paulistring += qbit[0].char.upper()
                qbit_list.append(i)
        self.make_empty()
        self.insert_pauli_string([paulistring,qbit_list,factor],exp=True)
        return self

    def make_empty(self):
        self.factor = 1
        self.qubits = [Qubit(name=str(i)) for i in range(self.n)]
        self.control_list = []

    def all_empty(self):
        """
        Check if all qubits have no gates.
        """
        check = True
        for b in self.qubits:
            if not b.is_empty():
                check = False
        return check

