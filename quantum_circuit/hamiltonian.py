import numpy as np
from .circuit import QuantumCircuit

class Hamiltonian:
    """
    Second quantized hamiltonian.

    Input:
        n (int) - Number of particle.
        l (int) - Number of spin orbitals.
    """
    def __init__(self,n,l):
        self.n = n
        self.l = l

    def set_integrals(self,one_body,two_body):
        self.h = one_body
        self.v = two_body

    def get_circuit(self):
        circuits = []
        # One-body interactions
        for i in range(self.n):
            for a in range(self.l):
                print('i:',i,'a:',a)
                if np.isclose(self.h[i,a],0) == False:
                    qc = QuantumCircuit(self.l)
                    qc.insert_one_body_operator(self.h[i,a],i,a)
                    print(qc)
                    circ = qc.transform_ladder_operators()
                    circuits.append(circ)
        # Two-body interactions
        for i in range(self.n):
            for j in range(i+1,self.n):
                for a in range(self.l):
                    for b in range(a+1,self.l):
                        if not np.isclose(self.v[i,j,a,b],0):
                            qc = QuantumCircuit(self.l)
                            qc.insert_two_body_operator(self.v[i,j,a,b],i,j,a,b)
                            circ = qc.transform_ladder_operators()
                            circuits.append(circ)
        return circuits


        
