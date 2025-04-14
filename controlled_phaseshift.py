from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import math
import numpy as np

# Příprava registru a obvodu pro 2 qubity
qubits = QuantumRegister(2, "q")
circuit = QuantumCircuit(qubits)

q0, q1 = qubits
# Superpozice na obou qubitech
circuit.h(q0)
circuit.h(q1)
# Kontrolovaný fázový posun o pi/2 rad na obou qubitech
circuit.cp(np.pi/2, q0, q1)

# Vykreslení obvodu a výsledného stavu
circuit.draw(output="mpl")
state = Statevector.from_instruction(circuit)
print("Statevector:", state)
plot_bloch_multivector(state.data)


plt.show(block=True)
