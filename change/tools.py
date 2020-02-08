from gates import X,Y


def get_permutations(n):
    """
    Give all possible (2^n) permutations of X and Y in an N-term chain.
    """
    from itertools import permutations
    ops = permutations('xy'*n,n)
    unique = []
    for op in ops:
        if op not in unique:
            unique.append(op)
    perms = []
    for elem in unique:
        new = []
        x = X(factor=0.5)
        y = Y(factor=0.5*complex(0,1)) 
        for o in elem:
            new.append(X(factor=0.5) if o == 'x' else Y(factor=0.5*complex(0,1)))
        perms.append(new)
    return perms

if __name__ == '__main__':
    L = get_permutations(2)
    print(L)
    for i in L:
        for j in i:
            print(id(j))

