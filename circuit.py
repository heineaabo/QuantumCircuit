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
        for i in range(len(self.mat)):
            self.mat[i].single_gate_optimization()
        # Remove unessecary Id gates
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

