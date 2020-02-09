from .gate import Gate

##################################################################################
#                       Info on implementation                                   #
#                                                                                #
# - When gates are in a tuple (gate1,gate2) they are acting on the same qubit.   #
# - When gates are in a list [gate1,gate2] they are acting in their own circuit. #
#   that is, the circuit will split in two.                                      #
#                                                                                #
##################################################################################

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
