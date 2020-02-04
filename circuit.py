from gates import *
from qubit import *

class QuantumCircuit:
    def __init__(self,n):
        self.mat = [Qubit(name=str(i)) for i in range(n)]
        self.control_circuit = []
        self.min_ctrl = 0 #Position of last controlled operation

    def apply(self,O,i=None):
        if isinstance(O,OneQubitGate):
            self.add_gate(O,i)
        if isinstance(O,ControlGate):
            ctrl,targ = O.get_connections()
            for j in range(len(self.mat)):
                self.mat[j].Identity()
            self.mat[ctrl].circ[-1] = CTRL(targ)
            self.mat[targ].circ[-1] = TARG(ctrl,O.gate)
            self.control_circuit.append(O) 
            self.min_ctrl = len(self.control_circuit)


    def add_gate(self,O,i):
        assert len(self.control_circuit) == len(self.mat[0].circ)
        if self.mat[i].act(O,self.min_ctrl):
            for j in range(len(self.mat)):
                if j != i:
                    self.mat[j].Identity()
            self.control_circuit.append(Id())

    def optimize(self):
        # Remove double action of same gate
        self.remove_double_occurrence()
        # Remove unessecary Id gates
        self.remove_identity()
        # Remove unessecary spaces
        self.move_back()

    def move_back(self):
        """
        Move gates to optimal position, between every controlled operation.
        """
        # Create empty spaces before controlled operations
        non_id = [i for i,gate in enumerate(self.control_circuit) if not isinstance(gate,Id)]
        if len(non_id) > 0:
            non_id.append(len(self.control_circuit)) # Add last entry so loop below works
            non_id.insert(0,0) # Add start entry so loop below works
            for a,b in zip(non_id[:-1],non_id[1:]):
                qubit_non_ids = []
                # Count number of non identity gates for each qubit in interval [a,b]
                for i in range(len(self.mat)):
                    n = self.mat[i].count_non_identity(a,b)
                    qubit_non_ids.append(n)
                # Move gates in interval back to a for each qubit
                for i in range(len(self.mat)):
                    self.


        # at end remove empty spaces

    def remove_double_occurrence(self):
        """
        Remove double action of same gate and makes them identity gates.
        """
        for i in range(len(self.mat)):
            self.mat[i].single_gate_optimization()

    def remove_identity(self):
        """
        Remove Identity if all qubits have identity in same place.
        """
        id_list = []
        for i in range(len(self.mat[0].circ)):
            if type(self.mat[0].circ[i]) == type(Id()):
                b = True
                for j in range(1,len(self.mat)):
                    if type(self.mat[j].circ[i]) != type(Id()):
                        b = False
                if b:
                    id_list.append(i)
        for i in range(len(self.mat)):
            self.mat[i].remove(id_list)
        for o in reversed(id_list):
            self.control_circuit.pop(o)

                
    def check_all_identity(self,d):
        check = True
        for i in range(len(self.mat)):
            if not isinstance(self.mat[i][d],Id):
                check = False
        return check

    def add_creation(self,l):
        """
        Add Jorda-Wigner transformed creation operator to qubit l.
        """
        n = len(self.mat)
        assert l < n
        if l > 0:
            for i in range(l):
                self.add_gate(Z(),i)
        self.add_gate(Create(),l)


    def add_annihilation(self,l):
        """
        Add Jorda-Wigner transformed annihilation operator to qubit l.
        """
        n = len(self.mat)
        assert l < n
        if l > 0:
            for i in range(l):
                self.add_gate(Z(),i)
        self.add_gate(Annihilate(),l)

    def __repr__(self):
        return str(self.mat)

    def __str__(self):
        string = 'Circuit:\n'
        for i,qbit in enumerate(self.mat):
            string += qbit.print_gates(self.control_circuit,i) + '\n'
        return string

