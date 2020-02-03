import numpy as np
from copy import deepcopy

class Gate:
    def __init__(self):
        self.char = ''
        self.factor = np.complex(1,0)

    def __eq__(self,other):
        if type(self) == type(other):
            if self.factor == other.factor:
                return True
            else:
                return False
        else:
            return False

    #def __mul__(self,other):
    #    if type(self) == type(other):
    #        return Identity()

    #def copy(self):
    #    return deepcopy(self)
    #
    def __repr__(self):
        return '{}{}'.format('i' if self.factor.imag != 0 else '',self.char.upper())

class OneQubitGate(Gate):
    def __init__(self):
        super().__init__()

class TwoQubitGate(Gate):
    def __init__(self):
        super().__init__()

# ONE-QUBIT GATES
class Id(OneQubitGate):
    def __init__(self):
        super().__init__()
        self.factor = 1
        self.char = 'I'

    def __mul__(self,other):
        return other.copy()

    def __rmul__(self,other):
        return other.copy()

class Pauli(OneQubitGate):
    def __init__(self):
        super().__init__()
        self.axis = ['x','y','z']
        self.r = None

    def __mul__(self,other):
        i = np.complex(0,1)
        if isinstance(other,complex):
            cp = self.copy()
            cp.factor *= i
            return cp
        if isinstance(other,Id):
            return self.copy()
        if isinstance(self, X):
            if isinstance(other, Y):
                return -i*Z()
            if isinstance(other, Z):
                return i*Y()
        if isinstance(self, Y):
            if isinstance(other, X):
                return i*Z()
            if isinstance(other, Z):
                return -i*X()
        if isinstance(self, Z):
            if isinstance(other, X):
                return i*Y()
            if isinstance(other, Y):
                return -i*X()

    def __rmul__(self,other):
        i = np.complex(0,1)
        if isinstance(other,complex):
            cp = self.copy()
            cp.factor *= i
            return cp

class X(Pauli):
    def __init__(self):
        super().__init__()
        self.char = 'X'

class Y(Pauli):
    def __init__(self):
        super().__init__()
        self.char = 'Y'

class Z(Pauli):
    def __init__(self):
        super().__init__()
        self.char = 'Z'

class H(OneQubitGate):
    def __init__(self):
        super().__init__()
        self.char = 'H'

# ROTATION GATES
class RotationGate(OneQubitGate):
    def __init__(self):
        super().__init__()
        self.axis = ''
        self.phi = 0

    def __eq__(self,other):
        eq_val = False
        if type(self) == type(other):
            if self.factor == other.factor:
                if self.axis == other.axis:
                    if self.phi == other.phi:
                        return True
        return eq_val

###
#Only considering pi/2 rotations.
#Dagger -> -pi/2
# TODO: Make for general phi
###
class Rx(RotationGate):
    def __init__(self,phi=1,dagger=False):
        super().__init__()
        self.axis = 'x'
        self.char = 'Rx'
        self.phi = phi
        self.dagger = dagger

class Ry(RotationGate):
    """
    Only considering pi/2 rotations.
    Dagger -> -pi/2
    """
    def __init__(self,phi=1,dagger=False):
        super().__init__()
        self.axis = 'y'
        self.char = 'Ry'
        self.phi = phi
        self.dagger = dagger

class Rz(RotationGate):
    """
    Only considering pi/2 rotations.
    Dagger -> -pi/2
    """
    def __init__(self,phi=1,dagger=False):
        super().__init__()
        self.axis = 'z'
        self.char = 'Rz'
        self.phi = phi
        self.dagger = dagger

# Jordan-Wigner
class Create(Gate):
    def __init__(self):
        super().__init__()
        self.char = '+'

class Annihilate(Gate):
    def __init__(self):
        super().__init__()
        self.char = '-'

# CONTROLLED GATES
class ControlGate(Gate):
    def __init__(self,gate,ctrl,targ):
        self.connection = None
        self.gate = gate
        self.char = 'C'+str(gate)
        self.targ = targ
        self.ctrl = ctrl
        self.factor = np.complex(1,0)

    def get_connections(self):
        return self.ctrl, self.targ

    def __eq__(self,other):
        eq_val = False
        if type(self) == type(other):
            if self.factor == other.factor:
                if self.gate == other.gate:
                    if self.targ == other.targ and self.ctrl == other.ctrl:
                        return True
        return eq_val


class CTRL(Gate):
    def __init__(self,targ):
        super().__init__()
        self.connection = targ
        self.char = '\u2A00'

class TARG(Gate):
    def __init__(self,ctrl,gate):
        super().__init__()
        self.connection = ctrl
        self.gate = gate
        if type(self.gate) == type(X()):
            self.char = '\u2A01'
        else:
            self.char = self.gate.char


