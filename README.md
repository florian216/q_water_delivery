# Optimising water delivery under constraints – CESQ Hackathon 2026

## 🌍 Context

Access to clean water remains one of humanity’s most pressing challenges. According to the UN, **one in four people** still lacks safely managed drinking water. In many regions, this scarcity is compounded by limited infrastructure, energy constraints, and geopolitical factors.

This repository presents a **combinatorial optimisation challenge** consisting in optimising water distribution under realistic constraints. This challenge was developed for the **European Center for Quantum Sciences hackathon (23–26 March 2026)**. It explores how variational quantum algorithms like **QAOA** and **VQE** can address combinatorial optimisation problems in resource allocation, with direct relevance to **UN Sustainable Development Goals 6, 7, and 13**.

---

## 🎯 Objective

Maximise water delivery to demand regions while respecting:
- **Source capacity limits**
- **Minimum regional demand**
- **Energy constraints** (limited number of active sources)

The problem is formulated as a **constrained binary optimisation**, mapped to a **QUBO/Hamiltonian** suitable for quantum processing units (QPUs).

---

## 📁 Repository Structure

```
.
├── README.md
├── CESQ_challenge_pres.pdf            # Presentation slides
├── CESQ_hackathon_challenge.pdf       # Full challenge description & mathematical model
├── administrative_regions.csv         # 11 regions: lat, lon, population
├── cities_51largest.csv               # 51 largest cities: lat, lon, population, admin status
├── main.py                            # Data generation: graphs & QUBO
├── plots.py                           # Graph plotting module
└── src/                               # (To be implemented) Quantum optimisation code and classical benchmarks
```

### Datasets

- **`administrative_regions.csv`**: GPS coordinates and population estimates for 11 administrative regions.
- **`cities_51largest.csv`**: Coordinates, population, and administrative centre status for the 51 most populated cities.

> ⚠️ Note: Connectivity edges between nodes are **not included** in the CSVs. They are generated programmatically (e.g., based on distance or fixed degree) to create pedagogical graph structures.

---

## 🧮 Mathematical Formulation

### Decision Variables
- $x_s \in \{0,1\}$: Source $s$ is active (1) or inactive (0)
- $x_r \in \{0,1\}$: Region $r$ is active (i.e. accepting water). Typically fixed to 1 in simplified models

### Objective Function
Maximise total water delivered:
$$
\max_{\vec{x}} \sum_{s \in \text{Sources}} \sum_{r \in \text{Regions}} w_{sr} x_s x_r.
$$

### Constraints (enforced via penalty terms)
1. **Source capacity**: $$ \sum_r w_{sr} x_r \leq w_s x_s $$
2. **Regional demand**: $$ \sum_s w_{sr} x_s \geq w_r x_r $$
3. **Energy limit**: $$ \sum_s x_s \leq S_{\text{max}} $$

### Hamiltonian (QUBO form)
$$
H = -\sum_{s,r} w_{sr} x_s x_r \\
    + \lambda_S \sum_s \left(-w_s x_s + \sum_r w_{sr} x_r\right) \\
    + \lambda_R \sum_r \left(+w_r x_r - \sum_s w_{sr} x_s\right) \\
    + \mu \left(S_{\text{max}} - \sum_s x_s\right)^2,
$$

where $\lambda_S, \lambda_R, \mu$ are Lagrange multipliers tuned empirically.

A more detail description of the mathematical modelling can be found in the file ```CESQ_hackathon_challenge.pdf```.

---

## 🔬 Proposed Approach

1. **Simplify**: Fix all regions as active ($x_r = 1$), reducing the problem to selecting optimal sources → **Knapsack-like formulation**.
2. **Encode**: Map the simplified problem to a QUBO.
3. **Solve**: Use **QAOA** or **VQE** on a simulator or real QPU.
4. **Scale**: Incrementally add complexity (e.g., variable region activation, dynamic edges).
5. **Optimise**: Apply parameter transfer, warm-starting, or scheduling strategies.

---

## 🛠️ Getting Started

*(Placeholder – to be implemented)*

```bash
# Clone the repo
git clone git@gitlab.com:YannBT/hackathon_cesq_challenge.git
cd hackathon_cesq_challenge

# Install dependencies (example)
pip install qiskit qiskit-optimization pennylane numpy pandas

# Run example (placeholder)
python src/run_qaoa.py --dataset cities_51largest.csv --max_sources 5
```


---

## 📈 Expected Outcomes

- A working quantum or hybrid classical-quantum pipeline for water allocation.
- Benchmarking against classical solvers (e.g., brute-force, simulated annealing).
- Insights into scalability, constraint handling, and parameter sensitivity.
- Pedagogical materials for students exploring quantum optimisation in sustainability contexts.

---

## 🤝 Contribution & License

- **Author**: Yann Beaujeault-Taudière  
- **License**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)  
- **Attribution**: Please credit the author and link to this repository if you build upon this work.

> This is a **non-commercial**, educational project developed for the CESQ Hackathon 2026. Real-world deployment would require integration with hydraulic models, real infrastructure data, and stakeholder validation.

---

## 📚 References

1. UN Water Facts (2025): https://www.unwater.org/water-facts  
2. Blekos et al., *A Review on QAOA* (2023): https://arxiv.org/abs/2306.09198  
3. Tilly et al., *VQE: Methods and Best Practices* (2021): https://arxiv.org/abs/2111.05176  

---

## Acknowledgements
The author thanks Cyrille Solaro and Stanimir Kondov for the invitation to mentor at the CESQ hackathon, and Tobias Denzler for the recommendation.


---

## 💡 Final Notes

> “Have fun!”, as reminded in the challenge brief.  
> Quantum computing is still emerging, but its potential to tackle real-world sustainability challenges is worth exploring—with rigor, creativity, and collaboration.


This README was generated automatically using Euria, the sovereign AI that protects your privacy and uses its energy to heat homes (https://euria.infomaniak.com).

The generated file was reviewed and corrected by the author.

— *Prepared for the CESQ Hackathon, March 2026*