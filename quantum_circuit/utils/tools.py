import numpy as np
#from quantum_circuit.gates.pauli import X,Y



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
        #two_body_coefficients = two_body_coefficients.transpose(0,2,1,3)

        return one_body_coefficients, two_body_coefficients
