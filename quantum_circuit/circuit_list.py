import numpy as np
from .gates import X,Y,Z,I

class PauliString:
    def __init__(self,factor,gates,qubits,measure=None,rev_eig=False):
        """
        factor: Factor of Pauli-string
        gates: Pauli gates in Pauli-string
        qubits: Qubits that pauli gates act on
        measure: List of qubits to measure
        rev_eig: If reverse measurement, 
                 that is parity gives - and + not + and -
        """
        assert factor.imag == 0
        self.factor = factor.real
        self.qubits = qubits
        self.gates = gates
        self.rev_eig = rev_eig # If reversed eigenvalue. 0=>-1, 1=>+1 
        if measure == None:
            self.measure_qubits = qubits
        

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
            for qubit in self.measure_qubits:
                if state[qubit] == '1':
                    eigval *= -1
            if self.rev_eig:
                eigval *= -1
            E += eigval*num_measure
        E /= shots
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

    def __getitem__(self,i):
        if len(self.qubits) == 0:
            return 0
        else:
            return self.qubits[i]

class QWCGroup:
    """
        Qubit-wise commuting group of Pauli strings.
    """
    def __init__(self,paulis=None,name='QWC'):
        self.paulis = paulis
        self.name = name
        if paulis == None:
            self.paulis = []
        self.ansatz = None

    def prepare(self,qc,qb,qa=None):
        if self.ansatz == None:
            self.find_ansatz()
        qc = self.ansatz.prepare(qc,qb,qa=qa)
        #for pauli_string in self.paulis:
        #    qc = pauli_string.prepare(qc,qb)
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
            string += str(pauli)+' '+self.name+'\n'
        return string[:-1]

    def __getitem__(self,i):
        return self.paulis[i]

    def __len__(self):
        return len(self.paulis)

    def __eq__(self,other):
        return False
    
    def find_ansatz(self):
        max_ = max([p[-1] for p in self.paulis]) # last qubit being acted on
        qubits = [i for i in range(max_ +1)]
        gates = [I() for i in range(max_ +1)]
        for p in self.paulis:
            for gate, qubit in zip(p.gates,p.qubits):
                if gate != I():
                    gates[qubit] = gate
        i = 0
        for gate in gates[::-1]:
            if gate == I():
                gates.pop(-i-1)
                qubits.pop(-i-1)
                i -= 1
            i += 1
        self.ansatz = PauliString(1,gates,qubits)

class GCGroup:
    """
        General commuting group of Pauli strings.
    """
    def __init__(self,paulis=None,name='GC'):
        self.paulis = paulis
        self.qubits = None
        if paulis == None:
            self.paulis = []

    def prepare(self,qc,qb):
        return self.ansatz(qc,qb,self.qubits)
    
    def set_ansatz(self,ansatz,qubits):
        """
            Set ansatz for simultaneous eigenbasis of the commuting operators.
        """
        self.ansatz = ansatz
        self.qubits = qubits

    def append(self,pauli,check_equal=False):
        if check_equal:
            if pauli in self.paulis:
                i = self.paulis.index(pauli)
                self.paulis[i].factor += pauli.factor
            else:
                self.paulis.append(pauli)
        else:
            self.paulis.append(pauli)

    def expectation(self,result,shots):
        E = 0
        for pauli_string in self.paulis:
            E += pauli_string.expectation(result,shots)
        return E

    def __len__(self):
        return len(self.paulis)

    def __eq__(self,other):
        return False

    def __str__(self):
        string = ''
        for pauli in sorted(self.paulis,key=len):
            string += str(pauli)+' '+self.name+'\n'
        return string[:-1]

class CircuitList:
    def __init__(self):
        self.num_gc = 0
        self.num_qwc = 0
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

    def __getitem__(self,i):
        return self.circuits[i]
    
    def __str__(self):
        string = ''
        for elem in self.circuits:
            string += str(elem)+'\n'
        return string[:-1]

    def __len__(self):
        return len(self.circuits)


