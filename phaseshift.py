from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import math

# Příprava kvantového obvodu na registru s 1 qubitem
qubits = QuantumRegister(1, "q")
circuit = QuantumCircuit(qubits)


q0 = qubits[0]
# Užití Hadamardovy brány
circuit.h(q0)
# Fázový posun o pi/2 rad
circuit.p(math.pi/2,q0)

# Vykreslení výsledného stavu na Blochovu kouli
state = Statevector.from_instruction(circuit)
print("Statevector:", state)
plot_bloch_multivector(state.data)


plt.show(block=True)