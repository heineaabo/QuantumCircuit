from gates import *
from printer import *

class Qubit:
    def __init__(self,name='q'):
        self.circ = []
        self.name = name

    def act(self,O,ctrl_pos=0):
        appended = False
        if len(self.circ) == 0 or ctrl_pos == len(self.circ):
            self.circ.append(O)
            appended = True
        elif self.all_Identity():
            self.circ[ctrl_pos] = O
        else:
            for i in reversed(range(ctrl_pos,len(self.circ))):
                # If last entry
                if isinstance(self.circ[i],Id):
                    if i == len(self.circ)-1:
                        self.circ[i] = O
                        break
                    else:
                        continue
                else:
                    if i == len(self.circ)-1:
                        self.circ.append(O)
                        appended = True
                        break
                    if i == ctrl_pos:
                        self.circ[i+1] = O 
                        break
                    else:
                        self.circ[i+1] = O
                        break
        return appended

    def Identity(self):
        self.circ.append(Id())

    def all_Identity(self):
        b = True
        for i in range(len(self.circ)):
            if not isinstance(self.circ[i],Id):
                b = False
        return b
    
    def single_gate_optimization(self):
        last_gate = None
        last_gate_index = None
        last_identity = False
        for i in range(0,len(self.circ)):
            if not isinstance(self.circ[i],Id):
                if type(self.circ[i]) == last_gate and last_gate_index != None\
                and not isinstance(self.circ[i],(CTRL,TARG)):
                    print(self.circ[i])
                    self.circ[i] = Id()
                    self.circ[last_gate_index] = Id()
                    last_gate_index = None
                    last_gate = None
                else:
                    last_gate = type(self.circ[i])
                    last_gate_index = i

    def remove(self,operations):
        for o in reversed(operations):
            self.circ.pop(o)
    
    def count_and_move(self,a,b):
        """
        Count number of identity gates in interval [a,b].
        Then Move all gates to its left-most controlled operation (or start).
        """
        Ids = []
        non_Ids = []
        count = 0
        # Count number ofi identity and non-identity gates
        for i in range(a,b):
            if isinstance(self.circ[i],Id):
                Ids.append(i)
            else:
                non_Ids.append(i)
                count += 1
        # If identity gates move all other gates
        if len(Ids) > 0:
            j = 0
            next_available = Ids[j]
            for i in non_Ids:
                if i <= next_available:
                    continue
                else:
                    # Swap elements
                    self.circ[i],self.circ[next_available] = self.circ[next_available], self.circ[i]
                    j += 1
                    if len(Ids[j:]) > 0:
                        if i < Ids[j]:
                            next_available = i
                        else:
                            z = Ids[j]
                            next_available = z
        return count

    def move_gates(self,a,b,n):
        """
        Move n number of gates to a and up.
        """
        for i in range(a,b):
            if isinstance(self.circ[i],Id):
                pass
                
    def __add__(self,other):
        """
        Combine circuit of two qubits.
        """
        if isinstance(other,Qubit):
            self.circ += other.circ            
            return self

    def __repr__(self):
        return str(self.circ)

    def __str__(self):
        return Printer(self).print_gates()

    def print_gates(self,control_list=None,q=None):
        return Printer(self).print_gates(control_list,q)

