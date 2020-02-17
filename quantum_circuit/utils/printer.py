#from quantum_circuit.gates.identity import I

class Printer:
    """
    TODO: Add for controlled gate.
    """
    #def __init__(self):
 
    #def print_circuit(self,circuit,eco=False):
    #    string = ''
    #    top = ''
    #    mid = ''
    #    bot = ''
    #    circ_len = circuit.register.get_length()
    #    if circ_len == 0:
    #        circ_len = 1
    #    for i in range(circuit.register.n):
    #        if eco:
    #            t,m,b = self.print_qubit(circuit.register[i],length=circ_len,eco=eco)
    #            top += t+'  '
    #            mid += m+'  '
    #            bot += b+'  '
    #        else:
    #            string += self.print_qubit(circuit.register[i],length=circ_len)
    #    if eco:
    #        return top +'\n'+mid+'\n'+bot+'\n' 
    #    else:
    #        return string

    def print_qubit(self,qubit,length,eco=False):
        top = ' '*(len(qubit.name)+3)
        mid = '\u2758{}\u27E9 '.format(qubit.name)
        bot = ' '*(len(qubit.name)+3)
        for gate in qubit.circ:
            if gate.is_identity():
                t,m,b = self.print_line()
            else:
                t,m,b = self.print_gate(gate)
            top += t
            mid += m
            bot += b
        for i in range(length - len(qubit.circ)):
            t,m,b = self.print_line()
            top += t
            mid += m
            bot += b
        if eco:
            return top,mid,bot
        else:
            return top+'\n'+mid+'\n'+bot+'\n'

    def print_control(self,up=False):
        """
        Print control qubit operation
        Up: True if control going upwards, false if downwards
        """
        #mb = '┬'
        #mt = '┴'
        #crs  = '┼'
        #tdot = '⫯' #\u2AEF
        #bdot = '⫰' #\u2AF0
        dot = '\u25CF'
        v  = '│'
        h  = '─'
        s  = ' '
        T = s
        M = dot
        B = v
        if up:
            T = v
            M = dot
            B = s
        top = s+s+s+T+s+s+s
        mid = h+h+h+M+h+h+h
        bot = s+s+s+B+s+s+s
        return top,mid,bot

    def print_line(self):
        h  = '─'
        s  = ' '
        top = s+s+s+s+s+s+s
        mid = h+h+h+h+h+h+h
        bot = s+s+s+s+s+s+s
        return top,mid,bot

    def print_gate(self,gate,c_up=False,c_down=False):
        rt = '┐'
        lt = '┌'
        lb = '└'
        rb = '┘'
        rv = '├' 
        lv = '┤'
        h  = '─'
        v  = '│'
        s  = ' '
        mb = '┬'
        mt = '┴'
        above = h
        below = h
        if c_up:
            above = mt
        if c_down:
            below = mb
        top = s + lt + h +   above   + h + rt + s
        mid = h + lv + s + gate.char + s + rv + h
        bot = s + lb + h +   below   + h + rb + s
        return top,mid,bot
    
    def print_identity(self,c=False):
        """
        c -> True if qubit is in between controlled operation
        """
        h  = '─'
        s  = ' '
        crs  = '┼'
        v  = '│'
        T = s
        M = h
        B = s
        if c:
            T = v
            M = crs
            B = v
        top = s+s+s+T+s+s+s
        mid = h+h+h+M+h+h+h
        bot = s+s+s+B+s+s+s
        return top,mid,bot


    def print_circuit(self,circuit,eco=False):
        # Assumed circuit is copmared to control list first
        # List with top, mid and bot for all qubits
        qubits = [['','',''] for i in range(circuit.register.n)]
        max_len = circuit.register.get_length()
        ctrl = False
        for i in range(max_len):
            if not circuit.register.control_list[i].is_identity():
                ctrl = True
                c = circuit.register.control_list[i].c
                t = circuit.register.control_list[i].t
                cgate = circuit.register.control_list[i].gate
            for j,q in enumerate(circuit.register):
                if ctrl:
                    if j == c:
                        if c < t:
                            top,mid,bot = self.print_control()
                        else:
                            top,mid,bot = self.print_control(up=True)
                    elif j == t:
                        top,mid,bot = self.print_gate(cgate,c_up=True)
                    elif c != -1 and t != -1 and  j < t and j > c:
                        top,mid,bot = self.print_identity(c=True)
                    else:
                        top,mid,bot = self.print_identity()
                else:
                    gate = q[i]
                    if gate.is_identity():
                        top,mid,bot = self.print_identity()
                    else:
                        top,mid,bot = self.print_gate(gate)
                qubits[j][0] += top
                qubits[j][1] += mid
                qubits[j][2] += bot
            ctrl = False
            c = -1
            t = -1
        string = ''
        for q in qubits:
            for l in q:
                string += l+'\n'
        return string
                

