import sys
sys.path.append('..')
from quantum_circuit import QuantumCircuit
from quantum_circuit.gates import X,Y,Z,I

qc1 = QuantumCircuit(2)
qc1(X(),0)
qc1(Y(),1)
qc2 = QuantumCircuit(2)
qc2(X(),0)
qc2(Y(),1)
qc3 = QuantumCircuit(2)
qc3(Y(),0)
qc3(Z(),1)
qc4 = QuantumCircuit(2)
qc4(Y(factor=complex(0,1)),0)
qc4(Z(),1)


assert qc1 == qc2
assert qc1 != qc3
assert qc2 != qc3

# Factor
qc3.factor *= complex(0,1)
assert qc3 == qc4

# empty
empty1 = QuantumCircuit(4)
empty1(I(),0)
empty2 = QuantumCircuit(4)
empty1(I(),1)
assert empty1 == empty2
empty2.factor = 3
assert empty1.register == empty2.register

q1 = QuantumCircuit(4)
q2 = QuantumCircuit(4)
q1(Z(),0)
q2(Z(),0)
assert q1 == q2

## Ladder operations
q1.insert_one_body_operator(1,1,3)
q2.insert_one_body_operator(1,1,3)
assert q1 == q2
q1.gate_optimization()
assert q1 != q2
q2.gate_optimization()
assert q1 == q2


