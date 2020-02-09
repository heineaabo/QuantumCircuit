from circuit import *
from qubit import *
from gates import *

class Optimizer:
    def __init__(self,circuit):
        self.circuit = circuit

    def run(self):
        # Remove double action of same gate
        self.remove_double_occurrence()
        # Remove unessecary Id gates
        self.remove_identity()
        # Remove unessecary spaces
        self.move_back()
        return self.circuit

    def move_back(self):
        """
        Move gates to optimal position, between every controlled operation.
        """
        # non_id => index of controlled operations
        non_id = [i for i,gate in enumerate(self.circuit.control_circuit) if not isinstance(gate,Id)]
        if len(non_id) > 0:
            # Add last entry so loop below works
            non_id.append(len(self.circuit.control_circuit)) 
            # Add start entry so loop below works
            if non_id[0] != 0:
                non_id.insert(0,0) 
            to_remove= []
            for a,b in zip(non_id[:-1],non_id[1:]):
                qubit_non_ids = []
                # Count number of non identity gates for each qubit in interval [a,b]
                for i in range(len(self.circuit.mat)):
                    qubit_non_ids.append(self.circuit.mat[i].count_and_move(a,b-1))
                # find indexes of identity gates
                for l in range(a+max(qubit_non_ids),b-1):
                    to_remove.append(l)
            # Remove identity gates
            for k in reversed(to_remove):
                for i in range(len(self.circuit.mat)):
                    self.circuit.mat[i].circ.pop(k)
                self.circuit.control_circuit.pop(k)
        else:
            qubit_non_ids = []
            to_remove= []
            a = 0
            b = len(self.circuit.mat[0].circ)
            # Count number of non identity gates for each qubit in interval [a,b]
            for i in range(len(self.circuit.mat)):
                qubit_non_ids.append(self.circuit.mat[i].count_and_move(a,b))
            # find indexes of identity gates
            for l in range(a+max(qubit_non_ids),b):
                to_remove.append(l)
            # Remove identity gates
            for k in reversed(to_remove):
                for i in range(len(self.circuit.mat)):
                    self.circuit.mat[i].circ.pop(k)
                self.circuit.control_circuit.pop(k)
        for i in range(len(self.circuit.mat)):
            assert len(self.circuit.mat[i].circ) == len(self.circuit.control_circuit)


    def remove_double_occurrence(self):
        """
        Remove double action of same gate and makes them identity gates.
        """
        for i in range(len(self.circuit.mat)):
            self.circuit.mat[i].single_gate_optimization()

    def remove_identity(self):
        """
        Remove Identity if all qubits have identity in same place.
        """
        id_list = []
        for i in range(len(self.circuit.mat[0].circ)):
            if type(self.circuit.mat[0].circ[i]) == type(Id()):
                b = True
                for j in range(1,len(self.circuit.mat)):
                    if type(self.circuit.mat[j].circ[i]) != type(Id()):
                        b = False
                if b:
                    id_list.append(i)
        for i in range(len(self.circuit.mat)):
            self.circuit.mat[i].remove(id_list)
        for o in reversed(id_list):
            self.circuit.control_circuit.pop(o)
