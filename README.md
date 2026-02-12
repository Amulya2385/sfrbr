# SFR-BR  
## Stability of Stateful Recovery under Bounded Resources

SFR-BR is a deterministic systems framework for analyzing the stability of stateful AI recovery under bounded hardware constraints.

It models how recovery policies behave when compute, memory, and cost budgets are limited — and identifies phase transitions where robustness shifts from beneficial to destabilizing.

---

# 🔍 Research Question

> Under bounded compute, does robustness enlarge the stability region — or destabilize the system?

SFR-BR answers this by:

- Deterministic recovery execution
- Hardware-aware cost accounting
- Latent corruption modeling
- Detection lag enforcement
- Stability phase sweeps
- Theoretical boundary derivation

---

# 🧠 Core Components

- RecoveryExecutor (bounded recovery)
- Hardware Constraint Vector (HCV)
- CostSimulator
- Latent KV-cache corruption
- Deterministic detection delay
- Elastic budget awareness (CostState)
- Stability phase experiments
- Theoretical stability inequality solver

All experiments are fully deterministic and reproducible.

---

# 📊 Stability Phase Diagram

We sweep:

- Context Depth (D)
- Hard Cost Cap (C)

Each grid point is classified as:

- Stable
- HardCap Failure

---

## 🔵 Stability Surface — Robust Agent

![Robust Stability Surface](figures/stability_surface_Robust.png)

---

## 🟡 Stability Surface — Cheap Agent

![Cheap Stability Surface](figures/stability_surface_Cheap.png)

---

# 🟢 Differential Stability Map

Regions where robustness expands or shrinks stability:

![Differential Stability Map](figures/differential_stability.png)

Legend:

- Green → Robust expands stability
- Red → Robust shrinks stability
- Gray → Equal stability

---

# 📈 Stability Boundary Curves

Maximum stable depth per hardware cap:

![Stability Boundary](figures/stability_boundary.png)

This figure shows:

- Empirical Cheap boundary
- Empirical Robust boundary
- Theoretical predicted boundary

---

# 🧮 Theoretical Stability Condition

We derive a sufficient stability inequality:

c_a · D + k · (D + 1/p) · log(D + 1/p) < C

Where:

- D = Context depth
- C = Hard cost cap
- c_a = Action cost coefficient
- k = KV recompute coefficient
- p = Detection probability

A numerical solver estimates theoretical collapse depth and compares it against empirical boundaries.

---

# 📊 Final Empirical Results

From final stability sweep:

- Total grid points: 56
- Cheap stable points: 6
- Robust stable points: 32
- Cheap stability ratio: 10.7%
- Robust stability ratio: 57.1%
- Net stability expansion: +26 regions

Robustness significantly enlarges the stability region under bounded compute in this configuration.

---

# 🏗️ Project Structure

SFR_BR_PROJECT/
│
├── agent/ # Agent policies (Cheap, Robust)
├── harness/ # Execution engine & cost modeling
├── experiments/ # Stability phase experiments
├── analysis/ # Boundary extraction & theory solver
├── plots/ # Publication-quality plot generators
├── config/ # System parameters
├── figures/ # Generated figures (PNG + PDF)
├── main.py # Final experiment runner
└── README.md

---

# ▶️ Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
Run final experiment:

python main.py


Figures will be generated and saved inside:

figures/

🔁 Determinism & Reproducibility

Fixed random seed

Deterministic detection delay

Explicit hardware cap enforcement

No black-box API calls

Fully replayable experiments

🎯 Contribution

SFR-BR provides:

A stability phase diagram for stateful recovery

A differential stability comparison (Cheap vs Robust)

Empirical collapse boundaries

Theoretical boundary validation

This framework formalizes when robustness improves stability — and when bounded compute induces collapse.