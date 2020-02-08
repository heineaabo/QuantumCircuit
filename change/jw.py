from circuit import QuantumCircuit

qc = QuantumCircuit(4)

qc.insert_one_body_operator(1,1,3)
print(qc)
qc.check_ladder()
qc.register.optimize()
print(qc)
