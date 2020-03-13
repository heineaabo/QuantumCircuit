import numpy as np
from .circuit import QuantumCircuit
from .utils import molecular2sec_quant
from .gates import X,Y,Rotation,Ph

class SecondQuantizedHamiltonian:
    def __init__(self,n,l,
                 one_body,two_body,exp=False,
                 nuclear_repulsion=None,anti_symmetric=False,add_spin=False,
                 conv=1):
        """
        Second quantized hamiltonian.

        Input:
            n (int)    - Number of particle.
            l (int)    - Number of spin orbitals.
            conv (bool/int) - Convention for occupied orbital
        """
        self.n = n
        self.l = l
        self.h = one_body
        self.v = two_body
        if add_spin:
            self.h,self.v = molecular2sec_quant(self.h,self.v)
        self.nuclear_repulsion = nuclear_repulsion
        if anti_symmetric:
            self.v *= 0.25

        self.exp = exp
        self.conv = conv 

        self.circuit = []
        self.get_circuit()

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
                    qc.insert_one_body_operator(self.h[p,q],p,q,
                                                conv=self.conv)
                    circ = qc.transform_ladder_operators()
                    circuits += circ
        # Two-body interactions
        for i in range(self.l):
            for j in range(self.l):
                for b in range(self.l):
                    for a in range(self.l):
                        if not np.isclose(self.v[i,j,b,a],0):
                            qc = QuantumCircuit(self.l)
                            qc.insert_two_body_operator(self.v[i,j,b,a],i,j,b,a,
                                                        conv=self.conv)
                            circ = qc.transform_ladder_operators()
                            circuits += circ
                                
        self.circuit = self.get_unique(circuits)

    def get_unique(self,circuits):
        #for i in circuits: print(repr(i))
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
            before = circ.factor
            if np.isclose(circ.factor,0):
                unique_circs.pop(i)
        final_circ = unique_circs
        if self.exp:
            exp_circ = QuantumCircuit(self.l)
            for circ in unique_circs:
                exp_circ += circ.to_exponent()
            final_circ = exp_circ
            final_circ.gate_optimization()
        return final_circ

    def to_circuit_list(self,ptype='vqe'):
        """
        Input:
            - ptype (str): How to represent gate actions
                - qiskit -> As qiskit gates (to be appended in a qiskit.QuantumCircuit)
                - vqe    -> As Qoperator in VQE takes in
                - openfermion -> As openfermion prints.
        """
        circuit_list = []
        if isinstance(self.circuit,QuantumCircuit):
            # single gate represented as [char,factor,qubit(,2nd qubit)]
            # with factor = 1 if not rotation gate
            control_list = self.circuit.register.control_list
            register = self.circuit.register
            for i,gate in enumerate(control_list):
                if gate.is_identity(): # Not control gates
                    for j,qbit in enumerate(register):
                        if i < len(qbit):
                            if not qbit[i].is_identity(): # No need to add identity gates
                                if isinstance(qbit[i],(Rotation,Ph)):
                                    circuit_list.append([qbit[i],
                                                         qbit[i].phi,
                                                         j])
                                else:
                                    circuit_list.append([qbit[i],1,j])

                else:
                    if isinstance(gate.gate,Rotation):
                        circuit_list.append([gate,
                                             gate.gate.phi,
                                             gate.c,
                                             gate.t])
                    else:
                        circuit_list.append([gate,1,gate.c,gate.t])
                    
        else:
            for circuit in self.circuit:
                circuit.defactor() # not necessary?
                new = [circuit.factor]
                for i,qbit in enumerate(circuit.register.qubits):
                    for gate in qbit.circ:
                        if not gate.is_identity():
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

