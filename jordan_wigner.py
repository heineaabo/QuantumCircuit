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


                








        

