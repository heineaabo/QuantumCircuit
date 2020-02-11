from quantum_circuit.gates import Gate,I
from quantum_circuit.gates.ladder import Creation,Annihilation

class Qubit:
    def __init__(self,name='q'):
        self.circ = []
        self.factor = 1
        self.name = name

    def __str__(self):
        string = ''
        if self.factor != 1:
            string += str(self.factor) + ' * '
        string += str(self.circ)
        return string

    def __repr__(self):
        return str(self.circ)

    def __eq__(self,other):
        if isinstance(other,Qubit):
            self.remove_identity()
            other.remove_identity()
            if len(self.circ) == len(other.circ):
                self.defactor()
                other.defactor()
                if self.factor == other.factor:
                    for i in range(len(self.circ)):
                        if self.circ[i] != other.circ[i]:
                            return False
                    return True
        return False

    def remove_identity(self):
        self.defactor()
        for i in reversed(range(len(self.circ))):
            if isinstance(self.circ[i],I):
                self.factor *= self.circ[i].factor
                self.circ.pop(i)


    def apply(self,gate,i=None):
        if i == None:
            self.circ.append(gate)
        else:
            self.circ.insert(0,gate)
            
    def optimize(self):
        if len(self.circ) > 0:
            new = [self.circ[0]]
            for i in range(1,len(self.circ)):
                gate1 = new[-1]
                gate2 = self.circ[i]
                gate = gate1*gate2
                if isinstance(gate,Gate):
                    new[-1] = gate
                elif isinstance(gate,tuple):
                    new[-1] = gate[0]
                    new.append(gate[1])
                elif isinstance(gate,list):
                    # Dont transform
                    new.append(gate2)
                else:
                    print(gate,gate1,gate2,new,self.circ,self.name)
                    raise ValueError('WRONG')
            factor = 1
            for i in reversed(range(len(new))):
                if isinstance(new[i],I):
                    factor *= new[i].factor
                    new.pop(i)
            self.circ = new
            self.factor *= factor

    def defactor(self):
        for i in range(len(self.circ)):
            # Add to qubit factor
            self.factor *= self.circ[i].factor
            # Defactor gate
            self.circ[i].factor = 1

    def get_all_ladder(self):
        """
        Returns position of all ladder operations on qubit.
        """
        num_ladder = 0
        ladder_operators = []
        for i,gate in enumerate(self.circ):
            if isinstance(gate,(Creation,Annihilation)):
                ladder_operators.append(i)
            else:
                continue
        return ladder_operators

    def is_empty(self):
        check = True
        for gate in self.circ:
            if not isinstance(gate,I):
                check = False
        return check
