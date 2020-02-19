import numpy as np
from .circuit import QuantumCircuit
from .gates import X,Y

class SecondQuantizedHamiltonian:
    def __init__(self,n,l):
        """
        Second quantized hamiltonian.

        Input:
            n (int)    - Number of particle.
            l (int)    - Number of spin orbitals.
        """
        self.n = n
        self.l = l
        self.circuit = []

    def set_integrals(self,one_body,two_body,nuclear_repulsion=None):
        self.h = one_body
        self.v = two_body
        self.nuclear_repulsion = nuclear_repulsion

    def get_circuit(self):
        circuits = []
        # Add nuclear repulsion as empty circuit
        if not self.nuclear_repulsion is None:
            rep = QuantumCircuit(self.l)
            rep.factor = self.nuclear_repulsion
            circuits.append(rep)
        # One-body interactions
        for p in range(self.l):
            for q in range(self.l):
                if not np.isclose(self.h[p,q],0):
                    qc = QuantumCircuit(self.l)
                    qc.insert_one_body_operator(self.h[p,q],p,q)
                    circ = qc.transform_ladder_operators()
                    circuits += circ
        # Two-body interactions
        for i in range(self.l):
            for j in range(self.l):
                for b in range(self.l):
                    for a in range(self.l):
                        if not np.isclose(self.v[i,j,b,a],0):
                            qc = QuantumCircuit(self.l)
                            qc.insert_two_body_operator(self.v[i,j,b,a],i,j,b,a)
                            circ = qc.transform_ladder_operators()
                            circuits += circ
                                
        self.circuit = self.get_unique(circuits)

    def get_unique(self,circuits):
        for i in reversed(range(len(circuits))):
            circ = circuits[i]
            circ.gate_optimization()
            circ.defactor()
            if np.isclose(circ.factor,0):
                circuits.pop(i) 
                continue
            circ.remove_identity()
        unique_circs = [circuits[0]]
        for i,circ1 in enumerate(circuits[1:]):
            check = False
            for j,circ2 in enumerate(unique_circs):
                if circ1.register == circ2.register:
                    check = True
                    unique_circs[j].factor += circ1.factor
            if not check:
                unique_circs.append(circ1)
        for i in reversed(range(len(unique_circs))):
            circ = unique_circs[i]
            if np.isclose(circ.factor,0):
                unique_circs.pop(i)
        return unique_circs

    def to_circuit_list(self,ptype='qiskit'):
        """
        Input:
            - ptype (str): How to represent gate actions
                - qiskit -> As qiskit gates (to be appended in a qiskit.QuantumCircuit)
                - vqe    -> As Qoperator in VQE takes in
                - opernfermion -> As openfermion prints.
        """
        circuit_list = []
        for circuit in self.circuit:
            circuit.defactor() # not necessary?
            new = [circuit.factor]
            for i,qbit in enumerate(circuit.register.qubits):
                for gate in qbit.circ:
                    if ptype == 'qiskit':
                        new.append([i,gate.to_qiskit()])
                    elif ptype == 'vqe':
                        new.append([i,gate.char.lower()])
                    elif ptype == 'openfermion':
                        new.append('{}{}'.format(gate.char,i))
            #if len(new) == 1:
            #    new.append([])
            circuit_list.append(new)
        return circuit_list


class ExponentialHamiltonian:
    def __init__(self,n,l):
        pass

