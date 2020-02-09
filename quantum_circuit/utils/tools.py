import numpy as np
from quantum_circuit.gates import X,Y


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

def molecular2sec_quant(one_body_integrals,two_body_integrals,EQ_TOLERANCE=1e-08):
        """Output arrays of the second quantized Hamiltonian coefficients.
        Note:
            The indexing convention used is that even indices correspond to
            spin-up (alpha) modes and odd indices correspond to spin-down
            (beta) modes.
        """
        n_qubits = 2 * one_body_integrals.shape[0]

        # Initialize Hamiltonian coefficients.
        one_body_coefficients = np.zeros((n_qubits, n_qubits))
        two_body_coefficients = np.zeros((n_qubits, n_qubits,
                                             n_qubits, n_qubits))
        # Loop through integrals.
        for p in range(n_qubits // 2):
            for q in range(n_qubits // 2):

                # Populate 1-body coefficients. Require p and q have same spin.
                one_body_coefficients[2 * p, 2 * q] = one_body_integrals[
                    p, q]
                one_body_coefficients[2 * p + 1, 2 *
                                      q + 1] = one_body_integrals[p, q]
                # Continue looping to prepare 2-body coefficients.
                for r in range(n_qubits // 2):
                    for s in range(n_qubits // 2):

                        # Mixed spin
                        two_body_coefficients[2 * p, 2 * q + 1,
                                              2 * r + 1, 2 * s] = (
                            two_body_integrals[p, q, r, s] / 2.)
                        two_body_coefficients[2 * p + 1, 2 * q,
                                              2 * r, 2 * s + 1] = (
                            two_body_integrals[p, q, r, s] / 2.)

                        # Same spin
                        two_body_coefficients[2 * p, 2 * q,
                                              2 * r, 2 * s] = (
                            two_body_integrals[p, q, r, s] / 2.)
                        two_body_coefficients[2 * p + 1, 2 * q + 1,
                                              2 * r + 1, 2 * s + 1] = (
                            two_body_integrals[p, q, r, s] / 2.)

        # Truncate.
        one_body_coefficients[
            np.absolute(one_body_coefficients) < EQ_TOLERANCE] = 0.
        two_body_coefficients[
            np.absolute(two_body_coefficients) < EQ_TOLERANCE] = 0.

        two_body_coefficients = np.einsum('pqsr',two_body_coefficients)

        return one_body_coefficients, two_body_coefficients
