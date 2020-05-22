import numpy as np
import sys
import os

def get_stabilizer_matrix(ops):
    for op in ops[1:]:
        assert len(op) == len(ops[0])
    M = len(ops)
    N = len(ops[0])
    S = np.zeros((2*N,M))
    for j,op in enumerate(ops):
        for i,gate in enumerate(op):
            if gate.lower() == 'x':
                S[N+i,j] = 1
            if gate.lower() == 'y':
                S[i,j] = 1
                S[N+i,j] = 1
            if gate.lower() == 'z':
                S[i,j] = 1
    return S,N

ops = []
for i in range(len(sys.argv[1:])):
    ops.append(sys.argv[i+1])

print(ops)

S,N = get_stabilizer_matrix(ops)

circ = []

while True:
    os.system('clear')
    print(S)
    action = input('Next action: ')
    if action.lower() == '':
        for i,A in enumerate(circ): print('{}: {}'.format(i,A))
        action = input('Next action: ')
    if action.lower() in ['quit','q','end']:
        break
    if action.lower() == 'done':
        print(circ)
        break
    #circ.append(action)
    #action = action.split('(')
    #action[1] = action[1][:-1]
    #action[1] = action[1].split(',')
    action = action.split(' ')
    if len(action[0]) > 1:
        for p in range(1,len(action[1:])+1,2):
            i = int(action[p])
            j = int(action[p+1])
            circ.append('{}({},{})'.format(action[0],i,j))
            if action[0].lower() == 'cx' or action[0].lower() == 'cnot':
                S[i] = np.remainder(S[i]+S[j],2)
                S[N+j] = np.remainder(S[N+i]+S[N+j],2)
            if action[0].lower() == 'cz':
                S[i,j] = 0
                S[j,i] = 0
            if action[0].lower() == 'swap':
                S[[i,j]] = S[[j,i]]
                S[[N+i,N+j]] = S[[N+j,N+i]]
    else:
        for p in range(1,len(action[1:])+1):
            i = int(action[p])
            circ.append('{}({})'.format(action[0],i))
            if action[0].lower() == 'h':
                S[[i,N+i]] = S[[N+i,i]]
            if action[0].lower() == 's':
                S[i,i] = 0
