import sys
sys.path.append('..')
from quantum_circuit.gates import *

# FOR REVERSED GATE PRODUCTS

### With int,float,complex
first = I()
first.factor *= 2
assert first == 2*I()
sec = X()
sec.factor *= -0.5
assert sec == -0.5*X()
thrd = Creation()
thrd.factor *= complex(0,1)
assert thrd == complex(0,1)*Creation()


### Not equal
assert I() != X()
assert I() != Y()
assert I() != Z()
assert I() != H()
assert I() != Rx()
assert I() != Ry()
assert I() != Rz()

assert X() != Y()
assert X() != Z()
assert Y() != Z()

assert X() != H()
assert Y() != H()
assert Z() != H()

### Identity
assert I()*I() == I()

assert X()*I() == X()
assert I()*X() == X()

assert Y()*I() == Y()
assert I()*Y() == Y()

assert Z()*I() == Z()
assert I()*Z() == Z()

assert H()*I() == H()
assert I()*H() == H()

assert I().is_identity() == True
assert X().is_identity() == False
assert Y().is_identity() == False
assert Z().is_identity() == False
assert H().is_identity() == False
assert Rx().is_identity() == False
assert Ry().is_identity() == False
assert Rz().is_identity() == False

### Pauli (Opposite of normal, since gates act to the left?)
i = complex(0,1)
assert X()*Y() == -i*Z()
assert Y()*X() == i*Z()

assert X()*Z() == i*Y()
assert Z()*X() == -i*Y()

assert Y()*Z() == -i*X()
assert Z()*Y() == i*X()

### Hadamard
assert H()*X() == (H(),X())
assert H()*Y() == (H(),Y())
assert H()*Z() == (H(),Z())
assert X()*H() == (X(),H())
assert Y()*H() == (Y(),H())
assert Z()*H() == (Z(),H())

### Creation and annihilation
assert Creation()*Creation() == Zero()
assert Annihilation()*Annihilation() == Zero()

assert Creation()*Annihilation() == [0.5*I(),0.5*Z()]
assert Annihilation()*Creation() == [0.5*I(),-0.5*Z()]

assert Creation()*X() == [(0.5)*I(),(0.5)*Z()]
assert Creation()*Y() == [(-0.5*i)*I(),(-0.5*i)*Z()]
assert Creation()*Z() == -Creation()
assert Creation()*H() == (Creation(),H())
assert X()*Creation() == [(0.5)*I(),(-0.5)*Z()]
assert Y()*Creation() == [(-0.5*i)*I(),(0.5*i)*Z()]
assert Z()*Creation() == Creation()
assert H()*Creation() == (H(),Creation())

assert Annihilation()*X() == [(0.5)*I(),(-0.5)*Z()]
assert Annihilation()*Y() == [(0.5*i)*I(),(-0.5*i)*Z()]
assert Annihilation()*Z() == Annihilation()
assert Annihilation()*H() == (Annihilation(),H())
assert X()*Annihilation() == [(0.5)*I(),(0.5)*Z()]
assert Y()*Annihilation() == [(0.5*i)*I(),(0.5*i)*Z()]
assert Z()*Annihilation() == -Annihilation()
assert H()*Annihilation() == (H(),Annihilation())

# Transform
assert Creation().transform() == [X(factor=0.5),Y(factor=-0.5*complex(0,1))]
assert Annihilation().transform() == [X(factor=0.5),Y(factor=0.5*complex(0,1))]

### Zero
assert Zero()*X() == Zero()
assert Zero()*X() == Zero()
assert Zero()*Y() == Zero()
assert Zero()*Z() == Zero()
assert Zero()*H() == Zero()
assert Zero()*I() == Zero()
assert Zero()*Creation() == Zero()
assert Zero()*Annihilation() == Zero()
assert Y()*Zero() == Zero()
assert Z()*Zero() == Zero()
assert H()*Zero() == Zero()
assert I()*Zero() == Zero()
assert Creation()*Zero() == Zero()
assert Annihilation()*Zero() == Zero()

# Rotation

assert Rx() == Rx()
assert Ry() == Ry()
assert Rz() == Rz()

assert Rx() != Ry()
assert Rx() != Rz()
assert Ry() != Rz()

assert Rx() != Rx(10)
assert Ry() != Ry(10)
assert Rz() != Rz(10)

# Control gates
assert CTRL(1) == CTRL(1)
assert TARG(1,X()) == TARG(1,X())

assert CTRL(1) != TARG(1,X())
assert CTRL(2) != CTRL(1)
assert TARG(1,X()) != TARG(2,X())
assert TARG(1,X()) != TARG(1,Y())


assert C(X(),0,1) == C(X(),0,1)
assert C(X(),1,2) != C(X(),0,1)
assert C(X(),0,1) != C(Y(),0,1)
