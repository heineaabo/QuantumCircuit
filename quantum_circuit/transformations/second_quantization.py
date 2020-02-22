from .. import QuantumCircuit
from ..gates import CNOT,H,Rx

def insert_one_body_operator(self,h,i,a):
    """
    Insert one-body second quantized operator on form:
        ⟨a∣h∣i⟩ a_a^\dagger a_i

    Input:
        i (int)    - Orbital to annihilate
        a (int)    - Orbital to create
        h (float)  - Matrix element
    """
    self.a(i)
    self.adg(a)
    self.factor *= h
QuantumCircuit.insert_one_body_operator = insert_one_body_operator

def insert_two_body_operator(self,v,i,j,a,b):
    """
    Insert two-body second quantized operator on form:
        ⟨ab∣h∣ij⟩ a_a^\dagger a_b^\dagger a_j a_i

    Input:
        i (int)    - Orbital to annihilate
        j (int)    - Orbital to annihilate
        a (int)    - Orbital to create
        b (int)    - Orbital to create
        v (float)  - Matrix element
    """
    self.a(i)
    self.a(j)
    self.adg(b)
    self.adg(a)
    self.factor *= v
QuantumCircuit.insert_two_body_operator = insert_two_body_operator

def insert_pauli_string(self,P,exp=False):
    """
    Insert Pauli string to circuit.
    Pauli string have form as the example below
            P = ['XXYX',[1,2,3,6],factor=1]
        where action corresponding to a qubit
            X -> on qubit 1
            X -> on qubit 2
            Y -> on qubit 3
            X -> on qubit 6
    """
    from math import pi
    if exp: # If exponent operator
        targ_qbit = P[1][-1]
        print(P[0],P[1])
        print(P[0][:-1],P[1][:-1])
        ind = len(self.register.control_list) # Index to insert gates before Rz gate
        self.rz(targ_qbit,P[2]) # On last qubit with rotation angle equal to factor
        for p,qbit in zip(P[0][:-1],P[1][:-1]):
            if p == 'X':
                self.insert_control_gate(CNOT(qbit,targ_qbit),ind)
                self.insert_single_gate(H(),qbit,ind)
                self.cx(qbit,targ_qbit)
                self.h(qbit)
            elif p == 'Y':
                self.insert_control_gate(CNOT(qbit,targ_qbit),ind)
                self.insert_single_gate(Rx(),qbit,ind)
                self.insert_single_gate(H(),qbit,ind)
                self.cx(qbit,targ_qbit)
                self.rx(qbit,phi=-pi/2)
                self.h(qbit)
            elif p == 'Z':
                self.insert_control_gate(CNOT(qbit,targ_qbit),ind)
                self.cx(qbit,targ_qbit)
        # Lastly apply for targ_qubit
        if P[0][-1] == 'X':
            self.insert_single_gate(H(),targ_qbit,ind)
            self.h(targ_qbit)
        if P[0][-1] == 'Y':
            self.insert_single_gate(Rx(),targ_qbit,ind)
            self.insert_single_gate(H(),targ_qbit,ind)
            self.rx(targ_qbit,phi=-pi/2)
            self.h(targ_qbit)
    else: # If not exponent operator
        for p,qbit in zip(P[0],P[1]):
            if p == 'X':
                self.x(qbit)
            if p == 'Y':
                self.y(qbit)
QuantumCircuit.insert_pauli_string = insert_pauli_string
