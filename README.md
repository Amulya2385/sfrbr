# SFR-BR
## Stability of Stateful Recovery under Bounded Resources

SFR-BR is a deterministic systems framework for analyzing the stability of stateful AI recovery under bounded hardware constraints.

It models how recovery policies behave when compute, memory, and cost budgets are limited — and identifies nonlinear phase transitions where recovery shifts from stable execution to infrastructure collapse.

---

# 🔍 Research Question

Under bounded compute, when does recovery succeed before infrastructure collapse — and when do resource limits induce failure?

SFR-BR reframes recovery as a resource-bounded dynamical system rather than a purely logical robustness problem.

---

# 🧠 Conceptual Overview

Modern AI agents operate with persistent internal state (e.g., KV-cache memory).  
When silent corruption occurs:

1. Corruption propagates undetected.
2. Detection occurs probabilistically.
3. Recovery triggers recomputation.
4. Recompute cost grows nonlinearly.
5. Hard infrastructure cap may be exceeded.
6. System collapses if cost ≥ cap.

Recovery stability therefore depends on:

- Corruption depth
- Detection delay
- Nonlinear recomputation growth
- Hard cost constraints

---

# 🧩 Core Components

- RecoveryExecutor — bounded recovery execution engine
- Hardware Constraint Vector (HCV) — explicit hard cost cap model
- CostSimulator — cumulative nonlinear cost accounting
- Latent KV-cache corruption model
- Geometric detection delay process
- Stability phase experiment framework
- Theoretical stability inequality solver

All experiments are deterministic and reproducible.

---

# 📊 Stability Phase Experiment

We sweep across:

- Corruption Depth (D)
- Hard Cost Cap (C)
- Detection Probability (p)

Each grid point is classified as:

- Stable
- Infrastructure Collapse

This produces empirical stability phase diagrams.

---

## 🟡 Stability Surface — Cheap Agent

![Cheap Stability Surface](figures/stability_surface_Cheap.png)

---

## 🔵 Stability Surface — Robust Agent

![Robust Stability Surface](figures/stability_surface_Robust.png)

---

# 🟢 Differential Stability Map

Regions where robustness expands or shrinks stability:

![Differential Stability Map](figures/differential_stability.png)

Legend:
- Green → Robust expands stability
- Red → Robust shrinks stability
- Gray → Equal stability

---

# 📈 Empirical vs Theoretical Stability Boundary

Maximum stable corruption depth per hardware cap:

![Stability Boundary](figures/stability_boundary.png)

This figure overlays:
- Empirical Cheap boundary
- Empirical Robust boundary
- Theoretical predicted boundary

Empirical collapse aligns qualitatively with the derived nonlinear inequality.

---

# 🧮 Theoretical Stability Condition

Total recovery cost is modeled as:

c_a · D + k · f(D)

Stable recovery requires:

c_a · D + k · f(D) < C

Where:

- D = Corruption depth
- C = Hard cost cap
- c_a = Linear action cost coefficient
- k · f(D) = Nonlinear recomputation growth

Infrastructure collapse occurs when:

c_a · D + k · f(D) ≥ C

Expected stability under probabilistic detection:

c_a · (1/p) + k · f(1/p) < C

Where p is detection probability.

A numerical solver estimates theoretical collapse depth and compares it with empirical phase boundaries.

---

# 📊 Final Empirical Results

From the final stability sweep:

- Total grid points evaluated: 56
- Cheap stable regions: 3
- Robust stable regions: 0
- Stability inversion observed under moderate detection probabilities
- Empirical collapse boundary matches nonlinear theoretical prediction

These results demonstrate that recovery stability is governed by bounded nonlinear cost accumulation rather than logical robustness alone.

---

# 🔁 Stability Inversion

Under specific detection probabilities and cost caps:

A cheaper recovery strategy remains stable  
while a robustness-aware strategy collapses due to additional overhead.

This inversion arises from nonlinear recomputation scaling interacting with hard cost constraints.

Robustness is therefore conditional under bounded compute.

---

# 🏗️ Project Structure

SFR_BR_PROJECT/

agent/        → Agent policies (Cheap, Robust)  
harness/      → Execution engine & cost modeling  
experiments/  → Stability phase sweeps  
analysis/     → Boundary extraction & inequality solver  
plots/        → Plot generation utilities  
config/       → System parameters  
figures/      → Generated figures (PNG + PDF)  
main.py       → Final experiment runner  
README.md  

---

# ▶️ Running the Project

Install dependencies:

pip install -r requirements.txt

Run the experiment:

python main.py

Generated figures will be saved in:

figures/

---

# 🔒 Determinism & Reproducibility

- Fixed random seed
- Deterministic corruption injection
- Explicit hard cap enforcement
- Controlled probabilistic detection model
- No external API calls
- Fully replayable parameter sweeps

---

# 🎯 Contribution

SFR-BR provides:

- A deterministic benchmark for stateful recovery under bounded compute
- Empirical stability phase diagrams
- Nonlinear collapse boundary extraction
- Stability inversion identification
- Analytical stability condition validation

This framework formalizes recovery as a bounded-resource phase transition problem and exposes structural limits of robustness under infrastructure constraints.

---

# 👩‍💻 Author

Amulya Biradar  
CSE (AI & ML)