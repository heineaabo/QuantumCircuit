from gates import *

class Qubit:
    def __init__(self,name='q'):
        self.circ = []
        self.factor = 1
        self.name = name

    def apply(self,gate,i=None):
        if i == None:
            self.circ.append(gate)
        else:
            self.circ.insert(0,gate)
            
    def optimize(self):
        new = [self.circ[0]]
        for i in range(1,len(self.circ)):
            gate1 = new[-1]
            gate2 = self.circ[i]
            gate = gate1*gate2
            #print('Iteration {}; {} * {} = {}; '.format(i,gate1,gate2,gate),end='')
            if isinstance(gate,Gate):
                new[-1] = gate
            elif isinstance(gate,tuple):
                new[-1] = gate[0]
                new.append(gate[1])
            elif isinstance(gate,list):
                # Dont transform
                new.append(gate1)
            else:
                raise ValueError('WRONG')
        self.circ = new

    def defactor(self):
        for i in range(len(self.circ)):
            # Add to qubit factor
            self.factor *= self.circ[i].factor
            # Defactor gate
            self.circ[i].factor = 1

    def get_all_ladder(self):
        """
        Returns position of all aldder operations on qubit.
        """
        num_ladder = 0
        ladder_operators = []
        for i,gate in enumerate(self.circ):
            if isinstance(gate,(Creation,Annihilation)):
                ladder_operators.append(i)
            else:
                continue
        return ladder_operators

    def __str__(self):
        string = ''
        if self.factor != 1:
            string += str(self.factor) + ' * '
        string += str(self.circ)
        return string

