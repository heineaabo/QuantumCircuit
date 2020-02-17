#from quantum_circuit.gates.identity import I

class Printer:
    """
    TODO: Add for controlled gate.
    """
    #def __init__(self):
 
    def print_circuit(self,circuit,eco=False):
        string = ''
        top = ''
        mid = ''
        bot = ''
        circ_len = circuit.register.get_length()
        if circ_len == 0:
            circ_len = 1
        for i in range(circuit.register.n):
            if eco:
                t,m,b = self.print_qubit(circuit.register[i],length=circ_len,eco=eco)
                top += t+'  '
                mid += m+'  '
                bot += b+'  '
            else:
                string += self.print_qubit(circuit.register[i],length=circ_len)
        if eco:
            return top +'\n'+mid+'\n'+bot+'\n' 
        else:
            return string

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

    def print_control(self,control_list=None,q=None):
        mb = '┬'
        mt = '┴'
        crs  = '┼'
        tdot = '⫯' #\u2AEF
        bdot = '⫰' #\u2AF0
        dot = '\u25CF'

    def print_line(self):
        h  = '─'
        s  = ' '
        top = s+s+s+s+s+s+s
        mid = h+h+h+h+h+h+h
        bot = s+s+s+s+s+s+s
        return top,mid,bot

    def print_gate(self,gate):
        rt = '┐'
        lt = '┌'
        lb = '└'
        rb = '┘'
        rv = '├' 
        lv = '┤'
        h  = '─'
        v  = '│'
        s  = ' '
        top = s + lt + h +      h    + h + rt + s
        mid = h + lv + s + gate.char + s + rv + h
        bot = s + lb + h +      h    + h + rb + s
        return top,mid,bot
    

