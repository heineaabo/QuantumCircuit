import numpy as np
from .gates import X,Y,Z

class PauliString:
    def __init__(self,factor,gates,qubits):
        self.factor = factor
        self.qubits = qubits
        self.gates = gates
        

    def prepare(self,qc,qb,qa=None):
        if qa == None:
            for gate,qubit in zip(self.gates,self.qubits):
                if gate.char != 'Z':
                    qc = gate.to_qiskit(qc,qb,qubit,transform=True)
                    #qc.append(gate.to_qiskit(transform=True),[qubit],[])
        else:
            for gate,qubit in zip(self.gates,self.qubits):
                qc = gate.to_qiskit(qc,qb,qubit,qa=qa,transform=False)
        return qc
   
    def expectation(self,result,shots):
        """ Interpret result from qiskit measurement. """
        E = 0
        for state,num_measure in result.items():
            state = state[::-1]
            eigval = 1
            for gate,qubit in zip(self.gates,self.qubits):
                if state[qubit] == '1':
                    eigval *= -1
            E += eigval*num_measure
        E /= shots
        #print(self,E*self.factor,result)
        return E*self.factor

    def __str__(self):
        return str([self.factor,[gate.char+str(i) for gate,i in zip(self.gates,self.qubits)]])

    def __eq__(self,other):
        """ Equality except factor """
        if not isinstance(other,PauliString):
            return False
        if len(self.gates) != len(other.gates):
            return False
        if self.gates == other.gates and self.qubits == other.qubits:
            return True
        return False

    def __len__(self):
        return len(self.gates)

class QWCGroup:
    """
        Qubit-wise commuting group of Pauli strings.
    """
    def __init__(self,paulis=None):
        self.paulis = paulis
        if paulis == None:
            self.paulis = []

    def prepare(self,qc,qb):
        for pauli_string in self.paulis:
            qc = pauli_string.prepare(qc,qb)
        return qc

    def expectation(self,result,shots):
        E = 0
        for pauli_string in self.paulis:
            E += pauli_string.expectation(result,shots)
        return E
    
    def append(self,pauli,check_equal=False):
        if check_equal:
            if pauli in self.paulis:
                i = self.paulis.index(pauli)
                self.paulis[i].factor += pauli.factor
            else:
                self.paulis.append(pauli)
        else:
            self.paulis.append(pauli)

    def __str__(self):
        string = ''
        for pauli in sorted(self.paulis,key=len):
            string += str(pauli)+'\n'
        return string[:-1]

    def __getitem__(self,i):
        return self.paulis[i]

    def __len__(self):
        return len(self.paulis)

    def __eq__(self,other):
        return False

class GCGroup:
    """
        General commuting group of Pauli strings.
    """
    def __init__(self,paulis):
        self.paulis = paulis

    def prepare(self,qc,qb):
        return self.ansatz(qc,qb)
    
    def set_ansatz(self,ansatz,outcomes):
        """
            Set ansatz for simultaneous eigenbasis of the commuting operators.
            Outcomes - what eigenstates corresponds to what operators.
                -> Integer entries correspond to computational basis states
                -> List entries correspond to operators where the eigenvalue 
                   is dependent on the integer entry eigenvalues.
        """
        self.ansatz = ansatz
        self.basis = [] # Operators that map to the eigenstates (comp basis)
        self.rest = []  # Operators that depend on the eigenstate operators
        for outcome in outcomes:
            if isinstance(outcome,list):
                self.rest.append(outcome)
            else:
                self.basis.append(outcome)

    def expectation(self,result,shots):
        print(result)
        E = np.zeros(len(self.paulis))
        for state,num_measure in result.items():
            state = state[::-1]
            eigvals = np.zeros(len(self.basis))
            for op,ind in enumerate(self.basis):
                eigval = 1 if state[ind] == '0' else -1
                eigvals[op] = eigval
                E[op] += eigval*num_measure*self.paulis[op].factor
            for i,elem in enumerate(self.rest):
                op = len(self.basis)+i
                eigval = 1
                for e in elem:
                    if not isinstance(e,str):
                        eigval *= eigvals[e]
                    else:
                        if e == '-':
                            eigval *= -1
                #print(state,num_measure,eigval*num_measure*self.paulis[op].factor/shots,self.paulis[op])
                E[op] += eigval*num_measure*self.paulis[op].factor
        print(E/shots)
        return np.sum(E)/shots

    def __len__(self):
        return len(self.paulis)

    def __eq__(self,other):
        return False

class CircuitList:
    def __init__(self):
        self.circuits = []

    def append(self,circuit,check_equal=False):
        if check_equal:
            if circuit in self.circuits:
                i = self.circuits.index(circuit)
                self.circuits[i].factor += circuit.factor
            else:
                self.circuits.append(circuit)
        else:
            self.circuits.append(circuit)
        #self.circuits.append(circuit)

    def groupz(self):
        to_remove = []
        z_group = QWCGroup()
        for i,circ in enumerate(self.circuits):
            if X() not in circ.gates and Y() not in circ.gates:
                to_remove.append(i)
        for i in to_remove[::-1]:
            circ = self.circuits[i]
            self.circuits.remove(circ)
            z_group.append(circ)
        self.circuits.insert(0,z_group)

    def __getitem__(self,i):
        return self.circuits[i]
    
    def __str__(self):
        string = ''
        for elem in self.circuits:
            string += str(elem)+'\n'
        return string[:-1]

    def __len__(self):
        return len(self.circuits)


