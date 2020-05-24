import numpy as np
from .circuit import QuantumCircuit
from .utils import molecular2sec_quant
from .gates import X,Y,Z,Rotation,Ph
from .circuit_list import CircuitList,PauliString,QWCGroup

class Hamiltonian:
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

class SecondQuantizedHamiltonian(Hamiltonian):
    def __init__(self,n,l,
                 one_body,two_body,exp=False,
                 nuclear_repulsion=None,anti_symmetric=False,add_spin=False,
                 conv=1):
        super().__init__(n,l,one_body,two_body,exp,
                         nuclear_repulsion,anti_symmetric,add_spin,conv)

        self.circuit = []
        self.get_circuit()
        #self.circuit_list = self.to_circuit_list('vqe')

    def get_circuit(self):
        circuits = []
        # Add nuclear repulsion as empty circuit
        if not self.nuclear_repulsion is None:
            rep = QuantumCircuit(self.l)
            rep.factor = self.nuclear_repulsion
            circuits.append(rep)
        # One-body interactions
        for p in range(self.l):
            if not np.isclose(self.h[p,p],0):
                qc = QuantumCircuit(self.l)
                circuits += qc.insert_one_body_operator(self.h[p,p],p,p,
                                            conv=self.conv)
        #for p in range(self.l):
        #    for q in range(self.l):
        #        if not np.isclose(self.h[p,q],0):
        #            qc = QuantumCircuit(self.l)
        #            qc.insert_one_body_operator(self.h[p,q],p,q,
        #                                        conv=self.conv)
        #            circ = qc.transform_ladder_operators()
        #            circuits += circ
        # Two-body interactions
        for i in range(self.l):
            for j in range(i+1,self.l):
                for a in range(self.l):
                    for b in range(a+1,self.l):
                        if not np.isclose(self.v[i,j,a,b],0):
                            qc = QuantumCircuit(self.l)
                            circuits += qc.insert_two_body_operator(4*self.v[i,j,a,b],i,j,a,b,conv=self.conv)
                                
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
                #if circ1.register == circ2.register:
                if circ1.equal_to(circ2): 
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

    def circuit_list(self,algorithm):
        """
        Return circuit list to specific algorithm.
        """
        if algorithm.lower() == 'qpe':
            circuit_list = []
            assert isinstance(self.circuit,QuantumCircuit)
            # single gate represented as [char,factor,qubit(,2nd qubit)]
            # with factor = 1 if not rotation gate
            control_list = self.circuit.control_list
            circuit = self.circuit
            for i,gate in enumerate(control_list):
                if gate.is_identity(): # No control gates
                    for j,qbit in enumerate(circuit.qubits):
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
                    
        elif algorithm.lower() == 'vqe':
            circuit_list = CircuitList()
            for circ in self.circuit:
                gates = []
                qubits = []
                for i,qbit in enumerate(circ.qubits):
                    if len(qbit) == 1:
                        gates.append(qbit[0])
                        qubits.append(i)
                circuit_list.append(PauliString(circ.factor,gates,qubits))
            circuit_list.groupz()
        else:
            raise ValueError('Input either "vqe" or "qpe"')
        return circuit_list

class PairingHamiltonian(Hamiltonian):
    def __init__(self,n,l,
                 one_body,two_body,exp=False,
                 nuclear_repulsion=0,anti_symmetric=False,add_spin=False,
                 conv=1):

        super().__init__(n,l,one_body,two_body,exp,
                         nuclear_repulsion,anti_symmetric,add_spin,conv)

        self.circuits = CircuitList()
        self.get_circuit()

    def get_circuit(self):
        # make x,y,z gate instances
        x,y,z = X(),Y(),Z()
        # Add nuclear repulsion to constant factor (can be 0)
        constant = self.nuclear_repulsion
        Zgroup = QWCGroup()
        # One-body interactions
        for p in range(self.l):
            if not np.isclose(self.h[p,p],0):
                factor = 0.5*self.h[p,p]
                constant += factor
                self.circuits.append(PauliString(-factor,[Z()],[p]),check_equal=True)
                #Zgroup.append(PauliString(-factor,[Z()],[p]),check_equal=True)
            for q in range(p+1,self.l):
                if not np.isclose(self.v[p,q,p,q],0):
                    factor = 0.25*self.v[p,q,p,q]
                    constant += factor

                    self.circuits.append(PauliString(-factor,[Z()],[p]),check_equal=True)
                    self.circuits.append(PauliString(-factor,[Z()],[q]),check_equal=True)
                    self.circuits.append(PauliString(factor,[Z(),Z()],[p,q]))
                    #Zgroup.append(PauliString(-factor,[Z()],[p]),check_equal=True)
                    #Zgroup.append(PauliString(-factor,[Z()],[q]),check_equal=True)
                    #Zgroup.append(PauliString(factor,[Z(),Z()],[p,q]))
        self.circuits.append(PauliString(constant,[],[]))
        #for pauli in Zgroup:
        #    self.circuits.append(pauli)
        #self.circuits.append(Zgroup)

        # Two-body interactions
        for p in range(self.l-1):
            for q in range(p+1,p+2):
                for r in range(q+1,self.l-1):
                    for s in range(r+1,r+2):
                        factor1 = 0.125*(self.v[p,q,r,s])
                        factor2 =-0.125*(self.v[p,q,r,s])
                        factor3 = 0.125*(self.v[p,q,r,s])
                        factor4 = 0.125*(self.v[p,q,r,s])

                        # Make Pauli strings
                        pqrs = [p,q,r,s]
                        xxxx, yyyy = [x,x,x,x], [y,y,y,y]
                        xxyy, yyxx = [x,x,y,y], [y,y,x,x]
                        xyyx, yxxy = [x,y,y,x], [y,x,x,y]
                        xyxy, yxyx = [x,y,x,y], [y,x,y,x]

                        if not np.isclose(factor1,0):
                            self.circuits.append(PauliString(factor1,xxxx,pqrs),check_equal=True)
                            self.circuits.append(PauliString(factor1,yyyy,pqrs),check_equal=True)
                        if not np.isclose(factor2,0):
                            self.circuits.append(PauliString(factor2,xxyy,pqrs),check_equal=True)
                            self.circuits.append(PauliString(factor2,yyxx,pqrs),check_equal=True)
                        if not np.isclose(factor3,0):
                            self.circuits.append(PauliString(factor3,xyyx,pqrs),check_equal=True)
                            self.circuits.append(PauliString(factor3,yxxy,pqrs),check_equal=True)
                        if not np.isclose(factor4,0):
                            self.circuits.append(PauliString(factor4,xyxy,pqrs),check_equal=True)
                            self.circuits.append(PauliString(factor4,yxyx,pqrs),check_equal=True)

    def circuit_list(self,algorithm):
        if algorithm.lower() == 'vqe':
            return self.circuits


