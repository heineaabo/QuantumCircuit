from .qubit import Qubit

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

         ---  Important  ---
    Implement gates using call method.
    """
    def __init__(self,n):
        self.n = n
        self.qubits = [Qubit(name=str(i)) for i in range(n)]
        self.control_list = []
        self.factor = 1
        self.printable_circuit = None

    def __repr__(self):
        return str(self.factor)+str(self.qubits)

    def __eq__(self,other):
        if isinstance(other,QuantumRegister):
            if self.n == other.n:
                self.defactor()
                other.defactor()
                if self.factor == other.factor:
                    check = []
                    for i in range(self.n):
                        if self.qubits[i] == other.qubits[i]:
                            check.append(True)
                        else:
                            check.append(False)
                    if sum(check) == self.n:
                        return True
        return False

    def __iter__(self):
        return iter(self.qubits)

    def __getitem__(self,i):
        if i > self.n:
            raise ValueError('Qubit {} not available in register with {} qubits.'.format(i,self.n))
        return self.qubits[i]

    def __call__(self,gate,q1,q2=None,phi=None):
        if q2 == None: # single qubit gate
            self.qubits[q1].apply(gate,q1,phi=phi)
            self.identity_layer(q1)

        else: # Control qubit gate
            pass

    ### REWRITE
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

    def all_empty(self):
        check = True
        for b in self.qubits:
            if not b.is_empty():
                check = False
        return check

