from .gate import Gate

class CTRL(Gate):
    def __init__(self,i):
        super().__init__()
        self.i = i
        self.char = 'C'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            return (self,other)
    
    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            return (other,self)

class TARG(Gate):
    def __init__(self,i):
        super().__init__()
        self.i = i
        self.char = 'T'

    def __mul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            return (self,other)
    
    def __rmul__(self,other):
        if isinstance(other,(int,float,complex)):
            self.factor *= other
            return self

        elif isinstance(other,Gate):
            return (other,self)
