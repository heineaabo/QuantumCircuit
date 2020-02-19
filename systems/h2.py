from openfermion.hamiltonians import MolecularData
from openfermionpsi4 import run_psi4
import numpy as np

from openfermion.hamiltonians import MolecularData
from openfermion.transforms import get_fermion_operator, get_sparse_operator, jordan_wigner
from openfermion.utils import get_ground_state
from openfermionpsi4 import run_psi4

import sys
sys.path.append('..')
from quantum_circuit import SecondQuantizedHamiltonian, QuantumCircuit
from quantum_circuit.utils import molecular2sec_quant

def openferm2circ(op):
    for i in str(op).split('\n'):
        print(i)



R = 0.7

geometry = [['H',[0,0,0]],
            ['H',[0,0,R]]]
molecule = MolecularData(geometry,'sto-3g',1,0)
molecule = run_psi4(molecule,run_fci=True)
h_pq = molecule.one_body_integrals
h_pqrs = molecule.two_body_integrals
nuc_repulsion = molecule.nuclear_repulsion
fci_energy = molecule.fci_energy

# OpenFermion Hamiltonian
molecular_hamiltonian = molecule.get_molecular_hamiltonian()
fermion_hamiltonian = get_fermion_operator(molecular_hamiltonian)
qubit_hamiltonian = jordan_wigner(fermion_hamiltonian)
qubit_hamiltonian.compress()
#print('The Jordan-Wigner Hamiltonian in canonical basis follows:\n{}'.format(qubit_hamiltonian))


h2_my = SecondQuantizedHamiltonian(2,4)
one,two = molecular2sec_quant(h_pq,h_pqrs)
h2_my.set_integrals(one,two,nuc_repulsion)
h2_my.get_circuit()
for i in h2_my.to_circuit_list(ptype='openfermion'): print(i)
print('openfermion')
openferm2circ(qubit_hamiltonian)

#for i,h1 in enumerate(one):
#    for j,h2 in enumerate(h1):
#        if h2 != 0:
#            print(i,j,h2)
#for i,h1 in enumerate(two):
#    for j,h2 in enumerate(h1):
#        for a,h3 in enumerate(h2):
#            for b,h4 in enumerate(h3):
#                if h4 != 0:
#                    print(i,j,a,b,' -> ',h4,'\t',h4/4)

