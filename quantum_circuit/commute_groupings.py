from .circuit_list import CircuitList,QWCGroup,GCGroup,PauliString
from .gates import X,Y,Z

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
CircuitList.groupz = groupz

def group_two_body(self):
    """ For two-body operators without Z-gates. """
    to_remove = []
    to_add = []
    c_group = GCGroup()
    for i,circ in enumerate(self.circuits):
        if not isinstance(circ,PauliString):
            continue
        if circ.gates == [X(),X(),X(),X()]:
            circ.measure_qubits = [3]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [X(),X(),Y(),Y()]:
            circ.measure_qubits = [2]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [X(),Y(),X(),Y()]:
            circ.measure_qubits = [1]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),X(),X(),Y()]:
            circ.measure_qubits = [0]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),Y(),Y(),Y()]:
            circ.measure_qubits = [0,1,2]
            circ.rev_eig = True
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),Y(),X(),X()]:
            circ.measure_qubits = [0,1,3]
            circ.rev_eig = True
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),X(),Y(),X()]:
            circ.measure_qubits = [0,2,3]
            circ.rev_eig = True
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [X(),Y(),Y(),X()]:
            circ.measure_qubits = [1,2,3]
            circ.rev_eig = True
            to_remove.append(i)
            to_add.append(circ)
    for i,circ in zip(to_remove[::-1],to_add[::-1]):
        self.circuits.remove(circ)
        c_group.append(circ)
    def ansatz(qc,qb):
        for i in range(3):
            qc.h(qb[i])
        # CX
        qc.cx(qb[0],qb[3])
        qc.cx(qb[1],qb[3])
        qc.cx(qb[2],qb[3])
        # CZ
        qc.cz(qb[2],qb[3])
        qc.cz(qb[1],qb[3])
        qc.cz(qb[0],qb[3])
        for i in range(4):
            qc.h(qb[i])
        return qc
    c_group.set_ansatz(ansatz)
    if len(c_group) > 0:
        self.circuits.insert(1,c_group)
CircuitList.group_two_body = group_two_body

def gokhale_two_body(self):
    """ For two-body operators without Z-gates. """
    to_remove = []
    to_add = []
    c_group = GCGroup()
    for i,circ in enumerate(self.circuits):
        if not isinstance(circ,PauliString):
            continue
        if circ.gates == [X(),X(),X(),X()]:
            circ.qubits = [3]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [X(),X(),Y(),Y()]:
            circ.qubits = [2]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [X(),Y(),X(),Y()]:
            circ.qubits = [1]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),X(),X(),Y()]:
            circ.qubits = [0]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),Y(),Y(),Y()]:
            circ.qubits = [1,2,3]
            circ.rev_eig = True
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),Y(),X(),X()]:
            circ.qubits = [0,2,3]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [Y(),X(),Y(),X()]:
            circ.qubits = [0,1,3]
            to_remove.append(i)
            to_add.append(circ)
        elif circ.gates == [X(),Y(),Y(),X()]:
            circ.qubits = [0,1,2]
            circ.rev_eig = True
            to_remove.append(i)
            to_add.append(circ)
    for i,circ in zip(to_remove[::-1],to_add[::-1]):
        self.circuits.remove(circ)
        c_group.append(circ)
    def gokhale_ansatz(qc,qb):
        for i in range(1,4):
            qc.h(qb[i])
        # Swap between 1 and 2
        qc.cx(qb[1],qb[2])
        qc.cx(qb[2],qb[1])
        qc.cx(qb[1],qb[2])
        #
        qc.cx(qb[1],qb[3])
        qc.cx(qb[2],qb[3])
        #
        qc.cx(qb[3],qb[0])
        qc.cx(qb[2],qb[0])
        qc.cx(qb[1],qb[0])
        # CZ
        qc.cz(qb[0],qb[3])
        qc.cz(qb[1],qb[3])
        qc.cz(qb[2],qb[3])
        for i in range(4):
            qc.h(qb[i])
        return qc
    c_group.set_ansatz(gokhale_ansatz)
    self.circuits.insert(1,c_group)
#CircuitList.group_two_body = gokhale_two_body
