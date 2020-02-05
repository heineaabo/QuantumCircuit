from circuit import *
from qubit import *
from gates import *
from jordan_wigner import *

import qiskit as qk

n = 2
l = 4
# singles
#circuits = []
#for i in range(n):
#    for a in range(n,l):
#        qc = QuantumCircuit(l)
#
#        qc.add_annihilation(i)
#        qc.add_creation(a)
#        qc.optimize()
#        [circuits.append(i) for i in transform_ladder_operators(qc)]
#
#for i in circuits:
#    #i.transform_to_pauli_z()
#    print(i)

circuits = []
for i in range(n):
    for a in range(n,l):
        qc = QuantumCircuit(l)
        qc.insert_pauli_string('XY_{}{}'.format(i,a),exp=True)
        qc.insert_pauli_string('YX_{}{}'.format(i,a),exp=True)
        circuits.append(qc)

qc.optimize()
print(qc)


