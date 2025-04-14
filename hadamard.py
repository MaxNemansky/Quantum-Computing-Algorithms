from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

# Příprava obvodu s kvantovým registrem o 1 qubitu
qubits = QuantumRegister(1, "q")
circuit = QuantumCircuit(qubits)

q0 = qubits[0]
# Užití Hadamardovy brány na qubit, stav je převeden do superpozice mezi |0> a |1>
circuit.h(q0)

# Zobrazení výsledné superpozice na Blochovu kouli
state = Statevector.from_instruction(circuit)
print("Statevector:", state)
plot_bloch_multivector(state.data)


plt.show(block=True)