from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import numpy as np

def QFT(circuit : QuantumCircuit, n_qubits):
    for i in range(n_qubits-1, -1, -1):
        circuit.h(i)

        for j in range(i-1, -1, -1):
            phi = (np.pi /(2**(i-j)))
            circuit.cp(phi, j, i)
    
    for i in range(n_qubits // 2):
        circuit.swap(i, n_qubits-1 -i)
    
    return circuit




if __name__ == "__main__":
    n_qubits = 4
    circuit = QuantumCircuit(n_qubits)
    state = np.zeros(16, dtype=complex)

    for idx in [0, 4, 8, 12]:
        state[idx] = 1/2

    circuit.initialize(state, [0, 1, 2, 3])
    #circuit.x(0)
    #circuit.x(2)
    circuit = QFT(circuit, n_qubits)

    state = Statevector.from_instruction(circuit)
    plot_bloch_multivector(state.data)

    circuit.draw(output="mpl")
    plt.show(block=True)
