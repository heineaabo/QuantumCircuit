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


class FermionHamiltonian(Hamiltonian):
    def __init__(self,n,l,
                 one_body,two_body,exp=False,
                 nuclear_repulsion=0,anti_symmetric=False,add_spin=False,
                 conv=1):

        super().__init__(n,l,one_body,two_body,exp,
                         nuclear_repulsion,anti_symmetric,add_spin,conv)

        self.circuit_list = CircuitList()
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
                Zgroup.append(PauliString(-factor,[Z()],[p]),check_equal=True)
            for q in range(p+1,self.l):
                if not np.isclose(self.v[p,q,p,q],0):
                    factor = 0.25*self.v[p,q,p,q]
                    constant += factor
                    Zgroup.append(PauliString(-factor,[Z()],[p]),check_equal=True)
                    Zgroup.append(PauliString(-factor,[Z()],[q]),check_equal=True)
                    Zgroup.append(PauliString(factor,[Z(),Z()],[p,q]))
        self.circuit_list.append(PauliString(constant,[],[]))
        #for pauli in Zgroup:
        #    self.circuit_list.append(pauli)
        self.circuit_list.append(Zgroup)

        # Two-body interactions
        for p in range(self.l):
            for q in range(p+1,self.l):
                for r in range(q+1,self.l):
                    for s in range(r+1,self.l):
                        factor1 = 0.125*(self.v[p,q,r,s]\
                                       + self.v[p,r,q,s]\
                                       + self.v[p,r,s,q])
                        factor2 =-0.125*(self.v[p,q,r,s]\
                                       - self.v[p,r,q,s]\
                                       - self.v[p,r,s,q])
                        factor3 = 0.125*(self.v[p,q,r,s]\
                                       + self.v[p,r,q,s]\
                                       - self.v[p,r,s,q])
                        factor4 = 0.125*(self.v[p,q,r,s]\
                                       - self.v[p,r,q,s]\
                                       + self.v[p,r,s,q])
                        # Make Pauli strings
                        pqrs = [p,q,r,s]
                        xxxx = [x,x,x,x]
                        yyyy = [y,y,y,y]
                        xxyy = [x,x,y,y]
                        yyxx = [y,y,x,x]
                        xyyx = [x,y,y,x]
                        yxxy = [y,x,x,y]
                        xyxy = [x,y,x,y]
                        yxyx = [y,x,y,x]
                        # Insert Z gates between p and q, and r and s
                        for k in range(r+1,s):
                            pqrs.insert(3,k)
                            xxxx.insert(3,z)
                            yyyy.insert(3,z)
                            xxyy.insert(3,z)
                            yyxx.insert(3,z)
                            xyyx.insert(3,z)
                            yxxy.insert(3,z)
                            xyxy.insert(3,z)
                            yxyx.insert(3,z)
                        for k in range(p+1,q):
                            pqrs.insert(1,k)
                            xxxx.insert(1,z)
                            yyyy.insert(1,z)
                            xxyy.insert(1,z)
                            yyxx.insert(1,z)
                            xyyx.insert(1,z)
                            yxxy.insert(1,z)
                            xyxy.insert(1,z)
                            yxyx.insert(1,z)

                        if not np.isclose(factor1,0):
                            self.circuit_list.append(PauliString(factor1,xxxx,pqrs),check_equal=True)
                            self.circuit_list.append(PauliString(factor1,yyyy,pqrs),check_equal=True)
                        if not np.isclose(factor2,0):
                            self.circuit_list.append(PauliString(factor2,xxyy,pqrs),check_equal=True)
                            self.circuit_list.append(PauliString(factor2,yyxx,pqrs),check_equal=True)
                        if not np.isclose(factor3,0):
                            self.circuit_list.append(PauliString(factor3,xyyx,pqrs),check_equal=True)
                            self.circuit_list.append(PauliString(factor3,yxxy,pqrs),check_equal=True)
                        if not np.isclose(factor4,0):
                            self.circuit_list.append(PauliString(factor4,xyxy,pqrs),check_equal=True)
                            self.circuit_list.append(PauliString(factor4,yxyx,pqrs),check_equal=True)


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
                qc.insert_one_body_operator(self.h[p,p],p,p,
                                            conv=self.conv)
                circ = qc.transform_ladder_operators()
                circuits += circ
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
                            qc.insert_two_body_operator(4*self.v[i,j,a,b],i,j,a,b,
                                                        conv=self.conv)
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
            control_list = self.circuit.register.control_list
            register = self.circuit.register
            for i,gate in enumerate(control_list):
                if gate.is_identity(): # No control gates
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
                    
        elif algorithm.lower() == 'vqe':
            circuit_list = CircuitList()
            for circ in self.circuit:
                gates = []
                qubits = []
                for i,qbit in enumerate(circ.register):
                    if len(qbit) == 1:
                        gates.append(qbit[0])
                        qubits.append(i)
                circuit_list.append(PauliString(circ.factor,gates,qubits))
            circuit_list.groupz()
        else:
            raise ValueError('Input either "vqe" or "qpe"')
        return circuit_list

