from .. import QuantumCircuit

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


