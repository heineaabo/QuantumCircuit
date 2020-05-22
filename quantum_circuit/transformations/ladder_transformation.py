from .. import QuantumCircuit,QuantumRegister,Qubit
from ..utils import get_permutations

def transform_ladder_operators(self):
    # Optimize circuit to minimize actions
    self.gate_optimization()

    # Find all ladder operators in circuit
    # with information about qubit and position on qubit.
    info = self.register.check_ladder()
    num = 0 # Number of new 
    each_ladder = []
    for elem in info:
        i = elem[0]
        for j in elem[1]: # If multiple ladder operators on qubit i
            num += 1
            each_ladder.append([i,j])

    # Transforming N ladder operators give 2^N new circuits (because of summations)
    copies = [self.copy() for i in range(2**num)]

    # Get all possible permutations of X and Y operators
    perms = get_permutations(num)
    assert len(copies) == len(perms)

    # One permutation to each copy
    for perm,circ in zip(perms,copies):
        for j,gate in enumerate(perm):
            qbit,ind = each_ladder[j]
            lad_gate = circ.register[qbit].circ[ind]
            gate.factor *= lad_gate.factor
            if (isinstance(lad_gate,Creation) and lad_gate.conv == 1) and isinstance(gate,Y):
                gate.factor *= -1
            elif (isinstance(lad_gate,Annihilation) and lad_gate.conv == 0) and isinstance(gate,Y):
                gate.factor *= -1
            circ.register[qbit].circ[ind] = gate

    # Optimize each copy
    for circ in copies:
        circ.gate_optimization()
        circ.defactor()

    # Sum all copies so that equivalent circuits are not evaluated multiple times.
    unique = [copies[0]]
    for circ1 in copies[1:]:
        check = False
        for circ2 in unique:
            if circ1.register == circ2.register:
                circ2.factor += circ1.factor
                check = True
                break
        if not check:
            unique.append(circ1)
    return unique
QuantumCircuit.transform_ladder_operators = transform_ladder_operators

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
QuantumRegister.check_ladder = check_ladder

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
Qubit.get_all_ladder = get_all_ladder

# Necessary imports 
from ..gates import X,Y, Creation,Annihilation
