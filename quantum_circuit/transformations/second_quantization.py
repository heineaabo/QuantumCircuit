from .. import QuantumCircuit
from ..gates import CNOT,H,Rx

def insert_one_body_operator(self,h,i,a,conv=1):
    """
    Insert one-body second quantized operator on form:
        ⟨a∣h∣i⟩ a_a^\dagger a_i

    Input:
        i (int)    - Orbital to annihilate
        a (int)    - Orbital to create
        h (float)  - Matrix element
        conv (bool/int) - Convention for occupied orbital
    """
    self.a(i,conv=conv)
    self.adg(a,conv=conv)
    self.factor *= h
QuantumCircuit.insert_one_body_operator = insert_one_body_operator

def insert_two_body_operator(self,v,i,j,a,b,conv=1):
    """
    Insert two-body second quantized operator on form:
        ⟨ab∣h∣ij⟩ a_a^\dagger a_b^\dagger a_j a_i

    Input:
        i (int)    - Orbital to annihilate
        j (int)    - Orbital to annihilate
        a (int)    - Orbital to create
        b (int)    - Orbital to create
        v (float)  - Matrix element
        conv (bool/int) - Convention for occupied orbital
    """
    self.a(i,conv=conv)
    self.a(j,conv=conv)
    self.adg(b,conv=conv)
    self.adg(a,conv=conv)
    self.factor *= v
QuantumCircuit.insert_two_body_operator = insert_two_body_operator

def insert_pauli_string(self,Pstr,exp=False):
    """
    Insert Pauli string to circuit.
    Pauli string have form as the example below
            Pstr = ['XXYX',[1,2,3,6],factor=1]
        where action corresponding to a qubit
            X -> on qubit 1
            X -> on qubit 2
            Y -> on qubit 3
            X -> on qubit 6
    On implementation:
        Acts with Rz gate first, then insert all gates before Rz 
        and acts with all gates after Rz instead of having two loops.
    """
    from math import pi
    # assure factor in Pstr
    if len(Pstr) == 2:
        Pstr.append(1)
    assert len(Pstr) == 3
    if exp: # If exponent operator
        if Pstr[0] == '' and len(Pstr[0]) == 0:
            self.ph(Pstr[2],0)
        else:
            targ_qbit = Pstr[1][-1]
            ind = len(self.register.control_list) # Index to insert gates before Rz gate
            self.rz(targ_qbit,Pstr[2]*2) # On last qubit with rotation angle equal to factor
            for p,qbit in zip(Pstr[0][:-1],Pstr[1][:-1]):
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
            if Pstr[0][-1] == 'X':
                self.insert_single_gate(H(),targ_qbit,ind)
                self.h(targ_qbit)
            if Pstr[0][-1] == 'Y':
                self.insert_single_gate(Rx(),targ_qbit,ind)
                self.insert_single_gate(H(),targ_qbit,ind)
                self.rx(targ_qbit,phi=-pi/2)
                self.h(targ_qbit)
    else: # If not exponent operator
        for p,qbit in zip(Pstr[0],Pstr[1]):
            if p == 'X':
                self.x(qbit)
            if p == 'Y':
                self.y(qbit)
QuantumCircuit.insert_pauli_string = insert_pauli_string
