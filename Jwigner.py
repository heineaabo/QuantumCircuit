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
                qc.add_annihilation(b)
                qc.add_annihilation(a)
                qc.add_creation(j)
                qc.add_creation(i)

qc.optimize()
print(qc)
qc.apply(Z(),0)
qc.apply(ControlGate(X(),1,3))
qc.apply(Y(),1)
qc.apply(X(),1)
qc.apply(Z(),0)
qc.apply(Y(),1)
qc.apply(ControlGate(X(),0,2))
qc.apply(Y(),1)
qc.apply(X(),2)
qc.apply(X(),2)
qc.optimize()
print(qc)
