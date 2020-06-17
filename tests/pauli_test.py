import sys
sys.path.append('..')
from quantum_circuit import PauliString,X,Y,Z

p1 = PauliString(1,[X(),Y(),Z()],[1,2,3])
p2 = PauliString(1,[X(),Y(),Z()],[1,2,4])
p3 = PauliString(1,[X(),Y(),Z()],[4,5,6])
p4 = PauliString(1,[X(),X(),Z()],[1,2,3])
p5 = PauliString(1,[X(),Y()],[1,2])


assert p1 != p2
assert p1 != p3
assert p1 != p4
assert p1 != p5


z1 = PauliString(0.5,[Z()],[0])
z2 = PauliString(0.123,[Z()],[1])
z3 = PauliString(0.4,[Z()],[0])
z4 = PauliString(0.4,[Z(),Z()],[0,1])

assert z1 != z2
assert z1 == z3
assert z1 != z4
assert z2 != z4
assert z3 != z4
