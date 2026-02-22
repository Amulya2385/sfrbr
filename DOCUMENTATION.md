# SFR-BR Documentation  
## Stability of Stateful Recovery under Bounded Resources

---

# 1. Executive Summary

SFR-BR is a deterministic benchmark framework for evaluating stateful recovery policies under bounded hardware constraints.

It models how AI agents behave when recovering from latent internal state corruption while operating under strict compute and memory budgets.

Unlike traditional robustness benchmarks that focus purely on logical correctness, SFR-BR treats recovery as a resource-bounded dynamical system.

The framework introduces:

- Stability phase diagrams
- Differential stability comparison (Cheap vs Robust)
- Empirical collapse boundary extraction
- Theoretical stability inequality derivation
- Stability inversion identification

SFR-BR formalizes when recovery remains feasible — and when bounded compute induces infrastructure collapse.

---

# 2. Problem Definition

Modern AI system evaluations often assume:

- Unlimited compute
- Instant failure detection
- Free recomputation
- No hard infrastructure limits

In real deployments:

- Compute is capped
- Memory is bounded
- Detection is delayed
- Recovery consumes resources
- Infrastructure failure can occur before logical recovery completes

This raises a systems-level question:

Under bounded compute, does increased robustness expand stability — or can it destabilize the system?

SFR-BR answers this using deterministic experimentation and analytical modeling.

---

# 3. System Architecture

The framework consists of four primary layers.

---

## 3.1 Agent Layer

Implements recovery strategies:

- BaseAgent (Cheap strategy)
- RobustAgent (Expanded defensive strategy)

Agents receive:

- Current execution state
- CostState (budget awareness)

Agents output deterministic Action objects.

Different agents may incur different nonlinear recomputation costs.

---

## 3.2 Harness Layer

Core execution components:

- RecoveryExecutor
- CostSimulator
- HardwareConstraintVector (HCV)
- CostState
- Snapshot

Responsibilities:

- Hard cost cap enforcement
- Action cost charging
- KV recompute charging
- Infrastructure collapse detection
- Deterministic step-by-step execution

Execution halts when cumulative cost exceeds the hard cap.

---

## 3.3 Failure Model

SFR-BR models latent corruption of contextual memory.

Features:

- KV cache poisoning
- Silent corruption propagation
- No immediate detection
- Probabilistic detection delay
- Recompute cost charged upon detection

Detection follows a geometric process with probability p per timestep.

Expected detection depth:

E[D] = 1 / p

Longer detection delays increase nonlinear recomputation burden.

---

## 3.4 Stability Classification

Each parameter configuration is classified as:

- Stable (recovery completes within hard cap)
- Infrastructure Collapse (cost ≥ cap)
- Logical Drift (semantic divergence, if triggered)

This enables construction of stability phase diagrams.

---

# 4. Stability Phase Framework

We sweep across:

- Corruption Depth (D)
- Hard Cost Cap (C)
- Detection Probability (p)

Each (D, C) configuration is evaluated deterministically.

Outputs include:

- Stability surface (per agent)
- Differential stability map
- Empirical collapse boundary curves

---

## 4.1 Stability Surface

For each agent:

Depth × Cap → Stable or Collapse

This produces a phase diagram separating stable and collapse regimes.

Nonlinear recomputation causes sharply curved collapse boundaries.

---

## 4.2 Differential Stability Map

Compares Cheap vs Robust strategies.

Regions are labeled as:

- Robust expands stability
- Robust shrinks stability
- Equal stability

This reveals crossover and inversion regimes.

---

## 4.3 Stability Boundary Extraction

For each hard cap value:

Maximum stable corruption depth is extracted.

This produces empirical collapse boundary curves.

These curves are later compared against the theoretical stability inequality.

---

# 5. Theoretical Stability Condition

Total recovery cost is modeled as:

C_total = c_a · D + k · f(D)

Where:

- D = Corruption depth
- C = Hard cost cap
- c_a = Linear action cost coefficient
- k · f(D) = Nonlinear recomputation growth term

Stable recovery requires:

c_a · D + k · f(D) < C

Infrastructure collapse occurs when:

c_a · D + k · f(D) ≥ C

Expected stability under probabilistic detection:

c_a · (1/p) + k · f(1/p) < C

This inequality defines a nonlinear collapse boundary in depth–cap space.

A numerical solver estimates theoretical collapse depth and compares it to empirical phase transitions.

---

# 6. Experimental Results

Final stability sweep:

- Total grid points evaluated: 56
- Cheap stable regions: 3
- Robust stable regions: 0
- Stability inversion observed under moderate detection probabilities

Key findings:

1. Stability regions exhibit sharp nonlinear collapse boundaries.
2. Increasing corruption depth rapidly triggers infrastructure collapse.
3. Detection delay significantly amplifies collapse risk.
4. Robust strategies may incur additional nonlinear overhead.
5. Inversion regimes exist where Cheap remains stable while Robust collapses.

Recovery stability is therefore governed by bounded nonlinear cost accumulation rather than logical correction capability alone.

---

# 7. Stability Inversion

Stability inversion occurs when:

Cheap strategy remains below hard cap  
while Robust strategy exceeds hard cap.

Formally:

c_a · D + k_A · f(D) ≥ C  
while  
c_a · D + k_B · f(D) < C  

where k_A > k_B.

This inversion arises from nonlinear recomputation scaling interacting with bounded hardware constraints.

Robustness is therefore conditional under bounded compute.

---

# 8. Determinism & Reproducibility

SFR-BR ensures:

- Deterministic corruption injection
- Explicit hard cap enforcement
- Controlled probabilistic detection
- Fixed parameter grids
- No external API calls
- Fully replayable experiments

All figures and stability surfaces are reproducible via:

python main.py

---

# 9. Development Evolution (Structured Iterations)

SFR-BR evolved through structured research iterations:

1. Deterministic execution engine
2. Hardware constraint modeling
3. Cost simulation integration
4. Latent KV corruption modeling
5. Probabilistic detection delay
6. Collapse boundary sweeps
7. Phase transition mapping
8. Differential stability comparison
9. Boundary curve extraction
10. Theoretical inequality derivation
11. Empirical-theoretical overlay validation
12. Stability inversion detection

Each iteration progressively refined the system into a formal stability benchmark.

---

# 10. Project Identity

SFR-BR is:

- A benchmark for stateful recovery under bounded compute
- A deterministic systems framework
- A stability phase analysis engine
- A nonlinear collapse boundary extractor
- A theoretical + empirical validation artifact

It is not merely a recovery simulator.

It is a stability mapping system for bounded AI recovery.

---

# 11. Conclusion

SFR-BR formalizes:

- When recovery policies remain stable
- When bounded compute induces collapse
- How nonlinear cost scaling shapes stability regions
- How empirical collapse aligns with theoretical inequality
- When robustness may destabilize under strict hardware limits

The framework provides a reproducible foundation for studying recovery stability in resource-constrained AI systems.


