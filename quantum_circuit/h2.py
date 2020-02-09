from openfermion.hamiltonians import MolecularData
from openfermionpsi4 import run_psi4
import numpy as np

from openfermion.hamiltonians import MolecularData
from openfermion.transforms import get_fermion_operator, get_sparse_operator, jordan_wigner
from openfermion.utils import get_ground_state
from openfermionpsi4 import run_psi4

from hamiltonian import Hamiltonian
from tools import molecular2sec_quant

R = 0.7

geometry = [['H',[0,0,0]],
            ['H',[0,0,R]]]
molecule = MolecularData(geometry,'sto-3g',1,0)
molecule = run_psi4(molecule,run_fci=True)
h_pq = molecule.one_body_integrals
h_pqrs = molecule.two_body_integrals
overlap = molecule.overlap_integrals
fci_energy = molecule.fci_energy
print(fci_energy)

# OpenFermion Hamiltonian
#molecular_hamiltonian = molecule.get_molecular_hamiltonian()
#fermion_hamiltonian = get_fermion_operator(molecular_hamiltonian)
#qubit_hamiltonian = jordan_wigner(fermion_hamiltonian)
#qubit_hamiltonian.compress()
#print('The Jordan-Wigner Hamiltonian in canonical basis follows:\n{}'.format(qubit_hamiltonian))

h2_my = Hamiltonian(2,4)
one,two = molecular2sec_quant(h_pq,h_pqrs)
h2_my.set_integrals(one,two)
circuit_list2 = h2_my.get_circuit()

#print('Open Fermion:')
#for i in circuit_list:
#    print(i)
#print('\n')
#print('My:')
#for i in circuit_list2:
#    print(i)
#print(h_pq)
#print(h_pqrs)
#for i in circuit_list:
#    for j in circuit_list2:
#        if i[1:] == j[1:]:
#            print('{:5f} {:5f} {:5f} {:5f} {}'.format(i[0],j[0].real,j[0].real*2,j[0].real*4,i[1:]))

#one = np.load('QS_one0714.npy')
#two = np.load('QS_two0714.npy')
#print(one,two)
#
#h2_qs = Hamiltonian(4)
##one_two = molecular2sec_quant(one,two)
#circuit_list3 = h2_qs.get_circuits(one,two)
for i in circuit_list:
    print(i)
for i in circuit_list2:
    print(i)



