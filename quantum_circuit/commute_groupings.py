from .circuit_list import CircuitList,QWCGroup,GCGroup,PauliString
from .gates import X,Y,Z,I

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
    # Find number of different qubit actions (Pauli-strings on different qubits)
    qubits = []
    for i,circ in enumerate(self.circuits):
        if not isinstance(circ,PauliString):
            continue
        if not circ.qubits in qubits:
            qubits.append(circ.qubits)
    for qbits in qubits:
        to_remove = []
        to_add = []
        c_group = GCGroup()
        for i,circ in enumerate(self.circuits):
            if not isinstance(circ,PauliString):
                continue
            if circ.qubits != qbits:
                continue
            if circ.gates == [X(),X(),X(),X()]:
                circ.measure_qubits = [qbits[3]]
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [X(),X(),Y(),Y()]:
                circ.measure_qubits = [qbits[2]]
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [X(),Y(),X(),Y()]:
                circ.measure_qubits = [qbits[1]]
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),X(),X(),Y()]:
                circ.measure_qubits = [qbits[0]]
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),Y(),Y(),Y()]:
                circ.measure_qubits = [qbits[0],qbits[1],qbits[2]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),Y(),X(),X()]:
                circ.measure_qubits = [qbits[0],qbits[1],qbits[3]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),X(),Y(),X()]:
                circ.measure_qubits = [qbits[0],qbits[2],qbits[3]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [X(),Y(),Y(),X()]:
                circ.measure_qubits = [qbits[1],qbits[2],qbits[3]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
        for i,circ in zip(to_remove[::-1],to_add[::-1]):
            self.circuits.remove(circ)
            c_group.append(circ)
        def ansatz(qc,qb,qbits):
            for i in range(3):
                qc.h(qb[qbits[i]])
            # CX
            qc.cx(qb[qbits[0]],qb[qbits[3]])
            qc.cx(qb[qbits[1]],qb[qbits[3]])
            qc.cx(qb[qbits[2]],qb[qbits[3]])
            # CZ
            qc.cz(qb[qbits[2]],qb[qbits[3]])
            qc.cz(qb[qbits[1]],qb[qbits[3]])
            qc.cz(qb[qbits[0]],qb[qbits[3]])
            for i in range(4):
                qc.h(qb[qbits[i]])
            return qc
        c_group.set_ansatz(ansatz,qbits)
        if len(c_group) > 0:
            c_group.name = 'GC'+str(self.num_gc)
            self.num_gc += 1
            self.circuits.insert(self.num_gc+self.num_qwc,c_group)
CircuitList.group_two_body = group_two_body


def group_two_body_IBM(self):
    """ For two-body operators without Z-gates. """
    """         For IBM 5-qubit computers       """
    # Find number of different qubit actions (Pauli-strings on different qubits)
    qubits = []
    for i,circ in enumerate(self.circuits):
        if not isinstance(circ,PauliString):
            continue
        if not circ.qubits in qubits:
            qubits.append(circ.qubits)
    for qbits in qubits:
        to_remove = []
        to_add = []
        c_group = GCGroup()
        for i,circ in enumerate(self.circuits):
            if not isinstance(circ,PauliString):
                continue
            if circ.qubits != qbits:
                continue
            if circ.gates == [X(),X(),X(),X()]:
                circ.measure_qubits = [qbits[1]]
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [X(),X(),Y(),Y()]:
                circ.measure_qubits = [qbits[1],qbits[2],qbits[3]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [X(),Y(),X(),Y()]:
                circ.measure_qubits = [qbits[3]]
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),X(),X(),Y()]:
                circ.measure_qubits = [qbits[0],qbits[1],qbits[3]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),Y(),Y(),Y()]:
                circ.measure_qubits = [qbits[0],qbits[2],qbits[3]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),Y(),X(),X()]:
                circ.measure_qubits = [qbits[0]]
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [Y(),X(),Y(),X()]:
                circ.measure_qubits = [qbits[0],qbits[1],qbits[2]]
                circ.rev_eig = True
                to_remove.append(i)
                to_add.append(circ)
            elif circ.gates == [X(),Y(),Y(),X()]:
                circ.measure_qubits = [qbits[2]]
                to_remove.append(i)
                to_add.append(circ)
        for i,circ in zip(to_remove[::-1],to_add[::-1]):
            self.circuits.remove(circ)
            c_group.append(circ)
        def ansatz(qc,qb,qbits):
            from math import pi
            # Optimized
            qc.u2(0,pi,qb[1])
            qc.cx(qb[1],qb[0])
            qc.cx(qb[1],qb[2])
            qc.cx(qb[1],qb[3])
            qc.u2(0,pi,qb[1])
            qc.cx(qb[1],qb[0])
            qc.cx(qb[1],qb[2])
            qc.cx(qb[1],qb[3])
            qc.u2(0,pi,qb[1])
            
            # Unoptimized
            #qc.u2(0,pi,qb[0])
            #qc.u2(0,pi,qb[2])
            #qc.u2(0,pi,qb[3])
            ## CX
            #qc.cx(qb[0],qb[1])
            #qc.cx(qb[2],qb[1])
            #qc.cx(qb[3],qb[1])
            ## CZ
            #qc.u2(0,pi,qb[1])
            #qc.cx(qb[0],qb[1])
            #qc.cx(qb[2],qb[1])
            #qc.cx(qb[3],qb[1])
            ## H
            #qc.u2(0,pi,qb[0])
            #qc.u2(0,pi,qb[2])
            #qc.u2(0,pi,qb[3])
            return qc
        c_group.set_ansatz(ansatz,qbits)
        if len(c_group) > 0:
            c_group.name = 'GC'+str(self.num_gc)+'-IBM'
            self.num_gc += 1
            self.circuits.insert(self.num_gc+self.num_qwc,c_group)
CircuitList.group_two_body_IBM = group_two_body_IBM

def find_qwc(self):
    not_all_checked = True
    self.circuits = self.circuits[::-1]
    k = 0
    while not_all_checked:
        max_len = len(max(self.circuits,key=len))
        group = QWCGroup()
        circ1 = self.circuits[k]
        if not isinstance(circ1,PauliString):
            k += 1
            continue
        to_remove = [k]
        to_add = [circ1]
        for i,circ2 in enumerate(self.circuits):
            if i == k: continue
            if not isinstance(circ2,PauliString): continue
            if all([commutation_pauli(circ_i,circ2,max_len=max_len) for circ_i in to_add]):
                #print(circ2)
                #for l in to_add: print(l)
                #print([commutation_pauli(circ_i,circ2,max_len=max_len) for circ_i in to_add])
                #print(circ1,circ2)
                to_remove.append(i)
                to_add.append(circ2)
        if len(to_remove) > 1:
            for i,circ in zip(to_remove[::-1],to_add[::-1]):
                self.circuits.remove(circ)
                group.append(circ)
            group.name = 'QWC'+str(self.num_qwc)
            self.num_qwc += 1
            k += 1
            self.circuits.insert(self.num_qwc,group)
        else:
            k += 1
        if k > len(self.circuits)-1:
            not_all_checked = False
CircuitList.find_qwc = find_qwc

def commutation_pauli(p1,p2,max_len=0,gc=False):
    # Make full gate lists with identity
    if len(p1) == 0 or len(p2) == 0:
        return True
    max_ = max([p.qubits[-1] for p in [p1,p2]]) # last qubit being acted on
    gates1 = [I() for i in range(max_ +1)]
    gates2 = [I() for i in range(max_ +1)]
    k1 = 0
    k2 = 0
    for g1,q1,g2,q2 in zip(p1.gates,p1.qubits,p2.gates,p2.qubits):
        gates1[q1] = g1
        gates2[q2] = g2
    c_num = 0
    for g1,g2 in zip(gates1,gates2):
        if not commutation(g1,g2):
            c_num += 1
    if gc and c_num%2 == 0: # GC
        return True
    elif not gc and c_num == 0: # QWC
        return True
    else:
        return False
        
def commutation(p1,p2):
    if p1.char == p2.char or I() in [p1,p2]: # Self commuting or one is identity
        return True
    return False

