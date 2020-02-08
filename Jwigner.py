from circuit import *
from qubit import *
from gates import *
from jordan_wigner import *

import sys

import qiskit as qk

n = 2 # particles
l = 4 # Spin orbitals

circuits = []


for i in range(l):
    for j in range(i+1,l):
        for a in range(l):
            for b in range(a+1,l):
                if (i,j,a,b) == (int(sys.argv[1]),
                                 int(sys.argv[2]),
                                 int(sys.argv[3]),
                                 int(sys.argv[4])):
                    qc = QuantumCircuit(l)

                    qc.add_annihilation(b)
                    qc.add_annihilation(a)
                    qc.add_creation(j)
                    qc.add_creation(i)

                    qc.optimize(jw=True)
                    qc.optimize()
                    print(qc)
                    break 
                    #[circuits.append(i) for i in transform_ladder_operators(qc)]

#print(len(circuits))
#for i,c in enumerate(circuits):
#    for j,d in enumerate(circuits):
#        if i == j:
#            print(c == -d)

#qc = QuantumCircuit(l)
#qc.apply(Z(),0)
#qc.apply(ControlGate(X(),1,3))
#qc.apply(Y(),1)
#qc.apply(X(),1)
#qc.apply(Z(),0)
#qc.apply(Z(),0)
#qc.apply(Y(),1)
#qc.apply(ControlGate(X(),0,2))
#qc.apply(Y(),1)
#qc.apply(X(),2)
#qc.apply(X(),2)
#qc.optimize()
#print(qc)
#
#qc_qk,qb,cb = qc.to_qiskit()
#print(qc_qk)
