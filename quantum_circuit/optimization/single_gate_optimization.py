from .. import QuantumCircuit,QuantumRegister,Qubit
from ..gates import CTRL,TARG,I,Rotation

# Qubit method
def squeeze(self):
    if len(self.circ) > 0:
        new = [self.circ[0]]
        for j in range(1,len(self.circ)):
            gate1 = new[-1]
            gate2 = self.circ[j]
            gate = gate1*gate2
            if isinstance(gate,tuple):
                new[-1] = gate[0]
                new.append(gate[1])
            elif isinstance(gate,list):
                # Dont transform
                new.append(gate2)
            elif isinstance(gate,I) and len(new) > 1:
                self.factor *= gate.factor
                new.pop(-1)
            elif gate == None:
                raise ValueError('Gate multiplication return None object {}*{} = None'.format(gate1,gate2))
            else:
                new[-1] = gate
        factor = 1
        for j in reversed(range(len(new))):
            if new[j].is_identity():
                factor *= new[j].factor
                new.pop(j)
        self.circ = new
        self.factor *= factor
Qubit.squeeze = squeeze

# Register methods
def update_control_list(self):
    num_control_op = len(self.control_list) - sum([g.is_identity() for g in self.control_list])
    # Isolate Controlled operations in control_list
    old_controls = []
    for g in self.control_list:
        if not g.is_identity():
            old_controls.append(g)
    # Find the corresponding CTRL and TARG gates
    ctrls = []
    targs = []
    c_inds = [0 for i in range(self.n)]
    t_inds = [0 for i in range(self.n)]
    for i,control_gate in enumerate(old_controls):
        c = control_gate.c
        t = control_gate.t
        for j,gate in enumerate(self.qubits[c].circ[c_inds[c]:]):
                if isinstance(gate,CTRL):
                    ctrls.append([c,j+c_inds[c]])
                    c_inds[c] += j+1
                    break
        for j,gate in enumerate(self.qubits[t].circ[t_inds[t]:]):
                if isinstance(gate,TARG):
                    targs.append([t,j+t_inds[t]])
                    t_inds[t] += j+1
                    break

    # Find circuit depth and make identity list
    new_control_list = []
    new_circ = [[] for i in range(self.n)]
    max_len = [len(q.circ) for q in self.qubits]
    inds = [0 for i in self.qubits]
    while max_len != inds:
        layer = []         # Layer for single gate
        control_layer = [] # Layer for controlled gates

        # Check if any single qubits
        single_gate = False
        for i,qbit in enumerate(self.qubits):
            if inds[i] >= len(qbit.circ):
                layer.append(I())
                control_layer.append(I())
                continue
            gate = qbit[inds[i]]
            if not isinstance(gate,(CTRL,TARG)):
                layer.append(gate)
                control_layer.append(I())
                inds[i] += 1
                single_gate = True
            elif isinstance(gate,(CTRL,TARG)):
                control_layer.append(gate)
                layer.append(I())
            else:
                layer.append(I())
                control_layer.append(gate)
        if single_gate:
            # If single gate in layer
            [new_circ[j].append(g) for j,g in enumerate(layer)]
            new_control_list.append(I())
        else:
            # If no single gate in layer
            c_ind = 0
            t_ind = 0
            # Find the ctrl partner to targ
            for j,g in enumerate(control_layer):
                if isinstance(g,TARG):
                    t_ind = j
                    c_ind = g.i
                    break
            # Put those in new_circ
            for j,g in enumerate(control_layer):
                if isinstance(g,CTRL):
                    if j != c_ind and j != t_ind: # could add inbetween gates here!"!"
                        if not g.is_identity(): # The gates not part of the controlled operation
                            control_layer[j] = I()
            if not (c_ind == 0 and t_ind == 0):
                # Add to inds to skip in next iteration
                inds[c_ind] += 1
                inds[t_ind] += 1
                [new_circ[j].append(g) for j,g in enumerate(control_layer)]
                # Add to new control_list
                for k,cgate in enumerate(self.control_list):
                    if not cgate.is_identity():
                        if c_ind == cgate.c and t_ind == cgate.t:
                            new_control_list.append(cgate)
                            self.control_list.pop(k)
                            break
            else:
                raise ValueError('Something wrong!')
        assert inds[0] <= max_len[0]

    self.printable_circuit = new_circ
    for i,qbit_circ in enumerate(new_circ):
        self[i].circ = qbit_circ

    self.control_list = new_control_list
QuantumRegister.update_control_list = update_control_list

def squeeze(self):
    for qbit in self.qubits:
        qbit.squeeze()
    self.update_control_list() # Maybe set printable_list as register?
QuantumRegister.squeeze = squeeze


