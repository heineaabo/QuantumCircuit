from circuit import *
from gates import *

qc1 = QuantumCircuit(4)
qc2 = QuantumCircuit(4)

qc1.apply(X(),1)
qc1.apply(Z(),3)
qc1.apply(ControlGate(X(),0,2))
print(qc1)

qc2.apply(X(),1)
qc2.apply(Z(),3)
qc2.apply(ControlGate(X(),0,2))
print(qc2)

qc1 = qc1 + qc2

qc1.apply(H(),0)
qc1.apply(ControlGate(X(),0,3))
print(qc1)

