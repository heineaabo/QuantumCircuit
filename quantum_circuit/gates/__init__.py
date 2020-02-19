from .gate import Gate
from .pauli import X,Y,Z
from .identity import I
from .hadamard import H
from .ladder import Creation,Annihilation
from .zero import Zero
from .control import CTRL,TARG,CNOT,C
from .rotation import Rotation,Rx,Ry,Rz

from .. import QuantumCircuit
def insert_single_gate(self,gate,qbit,ind):
    """Insert gate to qubit circuit at index ind"""
    for i in range(self.register.n):
        if i == qbit:
            self.register.qubits[i].circ.insert(ind,gate)
            continue
        self.register.qubits[i].circ.insert(ind,I())
    self.register.control_list.insert(ind,I())
QuantumCircuit.insert_single_gate = insert_single_gate

def insert_control_gate(self,control_gate,ind):
    """Insert gate to qubit circuit at index ind"""
    ctrl = CTRL(control_gate.t)
    targ = TARG(control_gate.c,control_gate.gate)
    self.register.control_list.insert(ind,control_gate)
    for i in range(self.register.n):
        if i == control_gate.c:
            self.register.qubits[i].circ.insert(ind,ctrl)
            continue
        if i == control_gate.t:
            self.register.qubits[i].circ.insert(ind,targ)
            continue
        self.register.qubits[i].circ.insert(ind,I())
    self.register.control_list.insert(ind,I())
QuantumCircuit.insert_control_gate = insert_control_gate

