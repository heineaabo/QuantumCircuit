
class Printer:
    """
    TODO: Add for controlled gate.
    """
    #def __init__(self):
 
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

    def print_control(self,up=False,extra=0):
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
        for i in range(extra):
            top += s
            mid += h
            bot += s
        return top,mid,bot

    def print_line(self,extra=0):
        h  = '─'
        s  = ' '
        top = s+s+s+s+s+s+s
        mid = h+h+h+h+h+h+h
        bot = s+s+s+s+s+s+s
        for i in range(extra):
            top += s
            mid += h
            bot += s
        return top,mid,bot

    def print_gate(self,gate,c_up=False,c_down=False,extra=0):
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

        k = len(gate.char)

        top = s + lt + h +   above*k   + h + rt + s
        mid = h + lv + s + gate.char + s + rv + h
        bot = s + lb + h +   below*k   + h + rb + s
        if extra != 0 and len(gate.char) == 1:
            for i in range(extra):
                top += s
                mid += h
                bot += s
        return top,mid,bot
    
    def print_identity(self,c=False,extra=0):
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
        for i in range(extra):
            top += s
            mid += h
            bot += s
        return top,mid,bot

    def print_circuit(self,circuit,eco=False):
        if circuit.register.printable_circuit == None:
            circuit.register.update_control_list()
        assert circuit.register.printable_circuit != None
        to_print = circuit.register.printable_circuit

        qubits = [['','',''] for i in range(circuit.register.n)]
        max_len = max([len(i) for i in to_print])
        ctrl = False
        for i in range(max_len):
            extra_space = self.check_all_qubit_chars(to_print,i)
            if not circuit.register.control_list[i].is_identity():
                ctrl = True
                c = circuit.register.control_list[i].c
                t = circuit.register.control_list[i].t
                cgate = circuit.register.control_list[i].gate
            for j,q in enumerate(to_print):
                if ctrl:
                    if j == c:
                        if c < t:
                            top,mid,bot = self.print_control(extra=extra_space)
                        else:
                            top,mid,bot = self.print_control(up=True,extra=extra_space)
                    elif j == t:
                        top,mid,bot = self.print_gate(cgate,c_up=True,extra=extra_space)
                    elif c != -1 and t != -1 and  j < t and j > c:
                        top,mid,bot = self.print_identity(c=True,extra=extra_space)
                    else:
                        top,mid,bot = self.print_identity(extra=extra_space)
                else:
                    gate = q[i]
                    if gate.is_identity():
                        top,mid,bot = self.print_identity(extra=extra_space)
                    else:
                        top,mid,bot = self.print_gate(gate,extra=extra_space)
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
                
    def check_all_qubit_chars(self,circuit,i):
        mx = 0
        for q in circuit:
            if len(q[i].char) > mx:
                mx = len(q[i].char)
        return mx-1

