from .qubit import Qubit
from quantum_circuit.gates import I,Z,Creation,Annihilation

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
        self.controls = []
        self.factor = 1

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

    ### Control listing
    def identity_layer(self,i,to_ctrl=True):
        """
        Add layer to circuit -> identity gates on all qubits except i.
        """
        self.controls.append(I())
        for j,q in enumerate(self.qubits):
            if j != i:
                q.apply(I())

    
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

    def optimize(self):
        for i in range(self.n):
            if len(self[i].circ) > 0:
                new = [self[i].circ[0]]
                for i in range(1,len(self[i].circ)):
                    gate1 = new[-1]
                    gate2 = self[i].circ[i]
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
                self[i].circ = new
                self[i].factor *= factor

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
                self(Z(),i)
            self(Creation(),qbit)

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
                self(Z(),i)
            self(Creation(),qbit)
   
    def all_empty(self):
        check = True
        for b in self.qubits:
            if not b.is_empty():
                check = False
        return check

