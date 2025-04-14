from qiskit import QuantumCircuit
from qiskit.primitives import BackendSamplerV2
from qiskit.compiler.transpiler import transpile
from qiskit.circuit import Gate
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qft import QFT
import random
from math import gcd, ceil
import numpy as np
from fractions import Fraction

def modular_exponentiation_gate(a, N, n_exponent, n_target):
    # Modulární exponenciace transformuje vstupní stav |x>|1> na stav |x>|(y * a^x) mod N>
    # Registr exponentu x je na qubitech 0,1,...,n-1
    # Registr exponenciace na qubitech n,n+1,...,n+target-1, kde targetem značíme počet bitů nutný k reprezentaci modulárního kódování

    # Komplexní reprezentace kvantové operace v dimenzích obvodu
    n_qubits = n_exponent + n_target
    dim = 2 ** n_qubits
    U = np.zeros((dim, dim), dtype=complex)
    
    # Výpočet modulárního exponentu na správných pozicích pomocí bitových operací
    for i in range(dim):
        x = i & ((1 << n_exponent) - 1) # x - bity exponentu
        y = i >> n_exponent # y - cílové bity modulární operace
        
        # Modulární operace pro bity náležející množině <0, N), jinak je operace nesmyslná
        if y < N:
            new_y = (y * pow(a, x, N)) % N
        else:
            new_y = y

        # Nový stav je sestaven z nového výsledku operace na y s ponecháním exponentu x na nižších bitech
        # | je bitový operátor OR, sloužící k zápisu x na nižší polohy v registru
        j = (new_y << n_exponent) | x
        # Nastavení hodnoty na správnou pozici v unitární matici
        U[j, i] = 1

    # Vytvoření vlastní qiskit brány z matice U, název je vytvořen ze základu a modula
    gate_name = f"modexp_{a}_mod_{N}"
    modexp_gate = Gate(name=gate_name, num_qubits=n_qubits, params=[])
    
    # Přiřazení qiskit definice pro bránu za užití unitárního obvodu
    modexp_circ = QuantumCircuit(n_qubits, name=gate_name)
    modexp_circ.unitary(U, list(range(n_qubits)), label=gate_name)
    modexp_gate.definition = modexp_circ
    return modexp_gate

# Klasická extrakce periody r z naměřených výsledků ze simulace
def extract_period_from_measurements(measured_vals, n_exponent, a, N):
    # Q - maximální hodnota na n bitech
    Q = 2 ** n_exponent
    # možní kandidáti na periodu r
    candidate_periods = []
    
    for m in measured_vals:
        phase = m / Q
        # Aproximace fáze zlomkem naměřené hodnoty a maximální hodnoty na n bitech
        # omezení fáze na dělitele N, jinak je výsledek nesmyslný
        frac = Fraction(phase).limit_denominator(N)
        r_candidate = frac.denominator

        # Výpis kandidáta a fáze
        print(f"m = {m}, p = {phase:.6f}, r = {r_candidate}")

        # Kontrola kandidáta na r pomocí podmínky mocniny na modulu N
        if r_candidate > 0 and pow(a, r_candidate, N) == 1:
            candidate_periods.append(r_candidate)
    
    if candidate_periods:
        # Návrat minimální kandidátní hodnoty r, jelikož má jít o nejmenší periodu
        r_final = min(candidate_periods)
        print("Kandidáti na periodu r z měření:", candidate_periods)
        return r_final
    
    print("Žádný vhodný kandidát na periodu r.")
    return None



def shor(N):
    # Výběr náhodného "a" mezi <2,N) nesoudělného s N
    a = random.randrange(2, N)
    while gcd(a, N) != 1:
        a = random.randrange(2, N)
    print("Zvolen základ a =", a)
    
    # n_target - počet qubitů nutný k reprezentaci N ve dvojkové soustavě
    # n_exponent - dvojnásobek bitů prvního čísla, užitý k modulární exponenciaci
    # total_qubits - celkový počet qubitů na registru
    n_target = ceil(np.log2(N))
    n_exponent = 2 * n_target
    total_qubits = n_exponent + n_target

    # Tvorba obvodu s kvantovým registrem
    # n_exponent zde značí počet bitů na klasickém registru, na něj je psáno v okamžiku měření
    qc = QuantumCircuit(total_qubits, n_exponent)
    

    # Inicializace výchozího stavu, element na registru exponenciace je ve stavu |1>
    # Poté jej brána modulární exponenciace využívá k výpočtu a zápisu výpočtu na mod N
    init_state = [0] * (2 ** n_target)
    init_state[1] = 1
    qc.initialize(init_state, list(range(n_exponent, total_qubits)))
    
    # Příprava superpozice na registrech exponenciace
    qc.h(range(n_exponent))
    
    # Tvorba brány modulární exponenciace
    # Vytváří superpozice všech stavů exponentu se základem "a" na modulu N
    modexp_gate = modular_exponentiation_gate(a, N, n_exponent, n_target)
    # Užití brány - stavy jsou nyní rozděleny a zmapovány na register exponentu x a register výsledku modulární operace
    qc.append(modexp_gate, list(range(total_qubits)))
    
    # Tvorba obvodu s diskrétní QFT
    # Ten je poté využit k tvorbě inverzní operace, která převádí z prostoru frekvenčního do časového
    qft_circ = QuantumCircuit(n_exponent, name="qft")
    qft_circ = QFT(qft_circ, n_exponent)
    inv_qft = qft_circ.inverse()
    qc.append(inv_qft, list(range(n_exponent)))
    
    # Měření stavů na registrech výsledku, ty jsou zapsány do klasického registru
    qc.measure(range(n_exponent), range(n_exponent))
    
    # Využití simulátoru QASM
    simulator = Aer.get_backend('qasm_simulator')
    print("Simulátor vytvořen")
    # Redukce obvodu na základní brány, jelikož simulátor nezná naši vlastnoruční bránu modulární exponenciace
    qc = transpile(qc, backend=simulator, basis_gates=simulator.configuration().basis_gates)
    print("Rozklad bran dokončen")
    # Sampler na sbírání výsledků
    sampler = BackendSamplerV2(backend=simulator)
    print("Sampler vytvořen")
    # Vykonání obvodu na sampleru, shots značí počet simulací
    job = sampler.run([qc], shots=128)
    print("Simulace zapsány")
    # Získání výsledků simulačních pokusů
    result = job.result()
    print("Výsledky spočteny")
    # Extrakce výsledků na klasickém registru v binární formě
    counts = result[0].data.c.get_counts()
    print("Výsledky měření simulací (binárně):")
    print(counts)
    
    # Překlad výsledků z binární soustavy do desítkové
    measured_vals = [int(bitstr, 2) for bitstr in counts.keys()]
    print("Výsledky měření simulací (desítkově):", measured_vals)
    
    # Klasické operace pro extrakci periody r
    r = extract_period_from_measurements(measured_vals, n_exponent, a, N)
    print("Odhadovaná perioda r =", r)
    
    # kontrola požadavků pro r: musí být sudé, a^r mod N == 1
    if r == None or r % 2 != 0 or pow(a, r, N) != 1:
        print("Vhodné r nebylo nalezeno. Spusťte program znovu.")
        return measured_vals

    # Výpočet rozkladu pomocí největšího společného dělitele
    factor1 = gcd(pow(a, r // 2) - 1, N)
    factor2 = gcd(pow(a, r // 2) + 1, N)
    print("Nalezený rozklad:", factor1, factor2)
    
    return measured_vals, factor1, factor2

if __name__ == "__main__":
    N = 21
    results = shor(N)
    print("\Výsledek:")
    print("Naměřené hodnoty (desítkově), kandidát na rozklad 1, kandidát na rozklad 2:")
    print(results)
