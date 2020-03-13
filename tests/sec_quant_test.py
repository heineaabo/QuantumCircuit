import sys
sys.path.append('..')
from quantum_circuit import QuantumCircuit,SecondQuantizedHamiltonian
from quantum_circuit.gates import *


assert Annihilation()*Z()*Z()*Creation() == Annihilation()*Creation()
assert Annihilation()*Creation() == Annihilation()*Creation()

assert X()*Y(factor=-complex(0,1)) == -1*Z()
assert Y(factor=complex(0,1))*X() == -1*Z()
assert Y(factor=complex(0,1))*Y(factor=-complex(0,1))


