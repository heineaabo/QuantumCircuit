from qubit import Qubit
from gates import *

class QuantumRegister:
    """
    Quantum register class.
    Handles all qubit action.

    Input:
        n (int) - Number of qubits.

    Attributes:
        n      (int)   - Number of qubits.
        qubits (List)  - List storing all qubits.
        factor (float) - Total factor of all qubits.
    """
    def __init__(self,n):
        self.n = n
        self.qubits = [Qubit(name=str(i)) for i in range(n)]
        self.factor = 1

    def get_length(self):
        l = []
        for i in range(len(self.qubits)):
            l.append(len(self[i].circ))
        return max(l)

    def defactor(self):
        """
        Defactor all qubits to self.factor.
        """
        for i in range(self.n):
            # Defactor qubit
            self[i].defactor() 
            # Add to circuit factor
            self.factor *= self[i].factor
            self[i].factor = 1

    def optimize(self):
        for i in range(self.n):
            self[i].optimize()

    def check_ladder(self):
        """
        Returns information about qubits with ladder operators.
        """
        information =[]
        for i in range(self.n):
            info = self[i].get_all_ladder()
            if len(info) > 0:
                information.append([i,info])
        return information

    def __getitem__(self,i):
        if i > self.n:
            raise ValueError('Qubit {} not available in register with {} qubits.'.format(i,self.n))
        return self.qubits[i]
    
    def append(self,qbit,check_name=True):
        """
        Append a qbit to register.

        Input:
            qbit (Qubit)      - Qubit to be appended
            check_name (bool) - Changes Qubit.name to its 
                                position in register.
        """
        if check_name:
            qbit.name = str(self.n)    
        self.qubits.append(qbit)
        self.n += 1

    def add_creation(self,qbit,transf='jw'):
        """
        Add transformed creation operator to qubit.

        Input:
            qbit (int) - Qubit to apply creation operator.
            transf (str) - Transformation type:
                    jw - Jordan-Wigner
                    bk - Braviy-Kitaev (TODO)
        """
        if transf.lower() == 'jw':
            for i in range(qbit):
                self[i].apply(Z())
            self[qbit].apply(Creation())

    def add_annihilation(self,qbit,transf='jw'):
        """
        Add transformed annihilation operator to qubit.

        Input:
            qbit (int) - Qubit to apply annihilation operator.
            transf (str) - Transformation type:
                    jw - Jordan-Wigner
                    bk - Braviy-Kitaev (TODO)
        """
        if transf.lower() == 'jw':
            for i in range(qbit):
                self[i].apply(Z())
            self[qbit].apply(Annihilation())
   
    
