from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

qubits = QuantumRegister(2, "q")
circuit = QuantumCircuit(qubits)

q0, q1 = qubits

circuit.h(q0)
#circuit.h(q1)
state = Statevector.from_instruction(circuit)
print("Statevector:", state)
#circuit.cx(q0, q1)
circuit.measure_all()
circuit.draw(output="mpl")
plot_bloch_multivector(state.data)


plt.show(block=True)

#print(circuit)