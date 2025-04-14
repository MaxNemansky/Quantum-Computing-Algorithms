from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

qubits = QuantumRegister(1, "q")
circuit = QuantumCircuit(qubits)

state = Statevector.from_instruction(circuit)
plot_bloch_multivector(state.data)


plt.show(block=True)

#print(circuit)