from circuit import QuantumCircuit

qc = QuantumCircuit(4)

qc.insert_one_body_operator(1,1,3)
#qc.insert_one_body_operator(1,0,1)
qc.gate_optimization()
circs = qc.transform_ladder()
for i in circs:
    print(i)
