#from quantum_circuit.gates import Gate,I,Creation,Annihilation

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

    def __getitem__(self,i):
        return self.circ[i]

    def __iter__(self):
        return iter(self.circ)

    def __len__(self):
        return len(self.circ)

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
            if self.circ[i].is_identity():
                self.factor *= self.circ[i].factor
                self.circ.pop(i)


    def apply(self,gate,i=None,phi=None):
        if i == None:
            self.circ.append(gate)
        else:
            self.circ.insert(i,gate)
            
    def defactor(self):
        for i in range(len(self.circ)):
            # Add to qubit factor
            self.factor *= self.circ[i].factor
            # Defactor gate
            self.circ[i].factor = 1

    def is_empty(self):
        check = True
        for gate in self.circ:
            if not gate.is_identity():
                check = False
        return check
