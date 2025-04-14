from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import math
import numpy as np


qubits = QuantumRegister(2, "q")
circuit = QuantumCircuit(qubits)

q0, q1 = qubits
circuit.h(q0)
circuit.h(q1)

circuit.p(math.pi/2,q0)
state0 = Statevector.from_instruction(circuit)
circuit.swap(q0, q1)

circuit.draw(output="mpl")
state1 = Statevector.from_instruction(circuit)
plot_bloch_multivector(state0.data)
plot_bloch_multivector(state1.data)


plt.show(block=True)
