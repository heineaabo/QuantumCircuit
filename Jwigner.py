from circuit import *
from qubit import *
from gates import *

n = 2 # particles
l = 4 # Spin orbitals

qc = QuantumCircuit(l)

for i in range(n):
    for j in range(i+1,n):
        for a in range(n,l):
            for b in range(a+1,l):
                #for k in range(i+1,j):
                #    qc.apply(Z(),k)
                #for k in range(a+1,b):
                #    qc.apply(Z(),k)
                
                qc.add_annihilation(b)
                qc.add_annihilation(a)
                qc.add_creation(j)
                qc.add_creation(i)

qc.apply(ControlGate(X(),0,2))
qc.optimize()
print(qc)
