from gates import *
from qubit import *
from circuit import *
import numpy as np

i = np.complex(0,1)

I = Id()
x = X()
y = Y()
z = Z()
h = H()

# Gates
assert I == I
assert x == x
assert y == y
assert z == z
assert h == h

assert x != I
assert y != I
assert z != I
assert x != y
assert x != z
assert y != z
assert h != x
assert h != y
assert h != z

# Identity multiplication
assert I*I == I
assert x*I == x
assert y*I == y
assert z*I == z

# Pauli multiplication
assert x*y == -i*z 
assert x*z == i*y 
assert y*x == i*z 
assert y*z == i*x 
assert z*x == -i*y 
assert z*y == -i*x 

# Controlled gates
cx = ControlGate(X(),0,1)
cx2 = ControlGate(X(),0,2)
cy = ControlGate(Y(),0,1)
cz = ControlGate(Z(),0,1)
ch = ControlGate(H(),0,1)

assert cx != cy
assert cx != cz
assert cy != cz
assert ch != cx
assert ch != cy
assert ch != cz

assert cx != cx2

# Rotation gates
rx = Rx()
ry = Ry()
rz = Rz()

assert rx != ry
assert rx != rz
assert ry != rz

# Qubit
circ = [I,I,I,I]
Q = Qubit(circ)
assert Q.all_Identity() == True

# Circuit
qc = QuantumCircuit(2)
qc.apply(z,0)
print(qc)
