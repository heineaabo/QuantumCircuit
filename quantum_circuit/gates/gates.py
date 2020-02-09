#import numpy as np
from qiskit.extensions.standard import IdGate, XGate, YGate, ZGate, HGate,\
                                       RXGate, RYGate, RZGate, CnotGate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################



class Gate:
    def __init__(self,factor=complex(1,0)):
        self.factor = factor
        self.char = ''

    def __eq__(self,other):
        if isinstance(other,Gate):
            if type(self) == type(other)\
                    and self.factor == other.factor:
                return True
            else:
                return False
        else:
            return False

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        else:
            raise ValueError('Can not multiply instance {} with instance {}'.format(type(self),type(other)))
        
    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        else:
            raise ValueError('Can not multiply instance {} with instance {}'.format(type(self),type(other)))

    def __neg__(self):
        self.factor *= -1
        return self

    def __repr__(self):
        return self.char
        
class I(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'I'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            other.factor *= self.factor
            return other

    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            other.factor *= self.factor
            return other

class Pauli(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)

    def __mul__(self,other):
        i = complex(0,1)
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,I):
            self.factor *= other.factor
            return self
        if isinstance(self, X):
            if isinstance(other, Y):
                new = Z(factor=self.factor*other.factor)
                return -i*new
            if isinstance(other, Z):
                new = Y(factor=self.factor*other.factor)
                return i*new
        if isinstance(self, Y):
            if isinstance(other, X):
                new = Z(factor=self.factor*other.factor)
                return i*new
            if isinstance(other, Z):
                new = X(factor=self.factor*other.factor)
                return -i*new
        if isinstance(self, Z):
            if isinstance(other, X):
                new = Y(factor=self.factor*other.factor)
                return -i*new
            if isinstance(other, Y):
                new = X(factor=self.factor*other.factor)
                return i*new
        if isinstance(other,H):
            return (self,other)
        if type(self) == type(other):
            new = I(factor=self.factor*other.factor)
            return new

class X(Pauli):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'X'
    
    def get_qiskit(self):
        return XGate()

class Y(Pauli):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'Y'

    def get_qiskit(self):
        return YGate()

class Z(Pauli):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'Z'

    def get_qiskit(self):
        return ZGate()

class H(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = 'H'
    
    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            if isinstance(other,I):
                self.factor *= other.factor
                return self
            else:
                return (self,other)
        else:
            raise ValueError('Can not multiply instance {} with instance {}'.format(type(self),type(other)))

    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Gate):
            if isinstance(other,I):
                self.factor *= other.factor
                return self
            else:
                return (other,self)
        else:
            raise ValueError('Can not multiply instance {} with instance {}'.format(type(self),type(other)))

    def get_qiskit(self):
        return HGate()


class Ladder(Gate):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)

class Creation(Ladder):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = '+'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Creation):
            return Zero()

        if isinstance(other,Annihilation):
            Id = I(factor=0.5*self.factor * other.factor)
            z = Z(factor=0.5*self.factor * other.factor)
            return [Id,z]
        if isinstance(other,Pauli):
            if isinstance(other,X):
                Id = I(factor=0.5*self.factor * other.factor)
                z = Z(factor=0.5*self.factor * other.factor)
                return [Id,z]
            if isinstance(other,Y):
                Id = I(factor=-0.5*complex(0,1)*self.factor * other.factor)
                z = Z(factor=-0.5*complex(0,1)*self.factor * other.factor)
                return [Id,z]
            if isinstance(other,Z):
                self.factor *= -other.factor
                return self
        if isinstance(other,H):
            return (self,other)

    def __rmul__(self,other):
        if isinstance(other,Z):
            self.factor *= other.factor
            return self

    def transform(self):
        x = X(factor=0.5*self.factor)
        y = Y(factor=-0.5*complex(0,1)*self.factor)
        return [x,y]


class Annihilation(Ladder):
    def __init__(self,factor=complex(1,0)):
        super().__init__(factor)
        self.char = '-'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self
        if isinstance(other,Annihilation):
            return Zero()

        if isinstance(other,Creation):
            Id = I(factor=0.5*self.factor*other.factor)
            z = Z(factor=-0.5*self.factor*other.factor)
            return [Id,z]
        
        if isinstance(other,Pauli):
            if isinstance(other,X):
                Id = I(factor=0.5*self.factor*other.factor)
                z = Z(factor=-0.5*self.factor*other.factor)
                return [Id,z]
            if isinstance(other,Y):
                Id = I(factor=0.5*complex(0,1)*self.factor*other.factor)
                z = Z(factor=-0.5*complex(0,1)*self.factor*other.factor)
                return [Id,z]
            if isinstance(other,Z):
                self.factor *= other.factor
                return self
        if isinstance(other,H):
            return (self,other)

    def __rmul__(self,other):
        if isinstance(other,Z):
            self.factor *= -other.factor
            return self


    def transform(self):
        x = X(factor=0.5*self.factor)
        y = Y(factor=0.5*complex(0,1)*self.factor)
        return [x,y]


class Zero(Gate):
    def __init__(self):
        super().__init__()
        self.factor = 0
