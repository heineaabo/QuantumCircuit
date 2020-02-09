from circuit import *
from gates import *
from qubit import *

def transform_ladder_operators(Qcirc):
    circuits = [Qcirc]
    check = True
    while check:
        new_check = []
        for i,qc in enumerate(circuits):
            if not qc.check_ladder():
               new_check.append(True) 
            else:
                new_check.append(False)
                circuits.append(qc.transform_ladder()) # Append new circuit to list, qc is changed
        if sum(new_check) == len(new_check):
            check = False
    return circuits


def simple_remove_z(qbit):
    """
    Simple optimization of qubit after JW-transformation.
    Will only work for circuits without control gates.
    Input:
        qbit (Qubit)
    
    TODO: Fix function to not general, not hard coded.

    """
    for i in reversed(range(1,len(qbit.circ))):
        gate = qbit.circ[i]
        gate2 = qbit.circ[i-1]
        if type(gate) == type(gate2) and not isinstance(gate,Id):
            qbit.circ[i] = Id()
            qbit.circ[i-1] = Id()
        elif isinstance(gate2,Annihilate) and isinstance(gate,Z):
            qbit.circ[i] = Id()
        elif isinstance(gate2,Z) and isinstance(gate,Create):
            qbit.circ[i-1] = Id()
    return qbit
            

        








        

