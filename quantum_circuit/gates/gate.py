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


    def is_identity(self):
        if self.char == 'I':
            return True
        return False
