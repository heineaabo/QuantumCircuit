import sys
sys.path.append('..')
from quantum_circuit import QuantumCircuit
from quantum_circuit.gates import X,Y,Z,I,H

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

## Easy gate act
q1 = QuantumCircuit(2)
q2 = QuantumCircuit(2)
q1(X(),0)
q2.x(0)

assert q1 == q2


## CNOT
qq = QuantumCircuit(3)
qq.h(0)
qq.h(1)
qq.cx(0,2)
qq.cx(1,2)
qq.z(2)
qq.cx(1,2)
qq.cx(0,2)
qq.h(0)
qq.h(1)
qq.gate_optimization()


qc1 = QuantumCircuit(3)
qc1.h(0)
qc1.h(1)
qc1.h(2)
qc1.x(1)
qc1.y(2)
qc2 = QuantumCircuit(3)
qc2.h(0)
qc2.h(2)
qc2.x(1)
qc2.y(2)
qc2.insert_single_gate(H(),1,0)
assert qc1 == qc2


expQC = QuantumCircuit(4)
expQC.insert_pauli_string(['XYXY',[0,1,2,3],1],exp=True)
expQC.gate_optimization()
print(expQC)
