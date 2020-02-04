from gates import *

class Printer:
    def __init__(self,qubit):
        self.qubit = qubit
 
    def print_gates(self,control_list=None,q=None):
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
        crs  = '┼'
        tdot = '⫯' #\u2AEF
        bdot = '⫰' #\u2AF0
        dot = '\u25CF'
        str_top = s*(len(self.qubit.name)+3)
        str_mid = '\u2758{}\u27E9 '.format(self.qubit.name)
        str_bot = s*(len(self.qubit.name)+3)
        for i,elem in enumerate(self.qubit.circ):
            if control_list == None:
                if isinstance(elem,Id):
                    top,mid,bot = self._print_no_gate()
                else:
                    top,mid,bot = self._print_gate(elem)
            else:
                if isinstance(control_list[i],Id):
                    if isinstance(elem,Id):
                        top,mid,bot = self._print_no_gate()
                    else:
                        top,mid,bot = self._print_gate(elem)
                else:
                    ctrl, targ = control_list[i].get_connections()
                    gate = control_list[i].gate
                    if isinstance(elem,CTRL):
                        top,mid,bot = self._print_ctrl()
                    elif isinstance(elem,TARG):
                        top,mid,bot = self._print_targ(gate)
                    elif q > ctrl and q < targ:
                        top,mid,bot = self._print_control_pass()
                    else:
                        top,mid,bot = self._print_no_gate()
            str_top += top
            str_mid += mid
            str_bot += bot

        str_top += s
        str_mid += h
        str_bot += s
        return str_top+'\n'+str_mid+'\n'+str_bot

    def _print_no_gate(self):
        s = ' '
        h = '─'
        top = s+s+s+s+s+s+s
        mid = h+h+h+h+h+h+h
        bot = s+s+s+s+s+s+s
        return top,mid,bot

    def _print_gate(self,gate):
        rt = '┐'
        lt = '┌'
        lb = '└'
        rb = '┘'
        rv = '├' 
        lv = '┤'
        h  = '─'
        s  = ' '
        top = s+lt+h+h+h+rt+s
        mid = h+lv+s+gate.char.upper()+s+rv+h
        bot = s+lb+h+h+h+rb+s
        return top,mid,bot
    
    def _print_ctrl(self):
        h  = '─'
        s  = ' '
        v = '│'
        tdot = '\u25CF'
        top = s+s+s+s+s+s+s
        mid = h+h+h+tdot+h+h+h
        bot = s+s+s+v+s+s+s
        return top,mid,bot

    def _print_targ(self,gate):
        rt = '┐'
        lt = '┌'
        lb = '└'
        rb = '┘'
        rv = '├' 
        lv = '┤'
        h  = '─'
        v  = '│'
        s  = ' '
        mt = '┴'
        char = gate.char.upper()
        top = s+lt+h+mt+h+rt+s
        mid = h+lv+s+char+s+rv+h
        bot = s+lb+h+h+h+rb+s
        if isinstance(gate,X):
            char = '\u2A01'
            top = s+s+s+v+s+s+s
            mid = h+h+h+char+h+h+h
            bot = s+s+s+s+s+s+s
        return top,mid,bot

    def _print_control_pass(self):
        """
        If control operation in circuit but not on qubit
        """
        h  = '─'
        s  = ' '
        v = '│'
        crs  = '┼'
        top = s+s+s+v+s+s+s
        mid = h+h+h+crs+h+h+h
        bot = s+s+s+v+s+s+s
        return top,mid,bot
