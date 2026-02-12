# SFR-BR Documentation  
## Stability of Stateful Recovery under Bounded Resources

---

# 1. Executive Summary

SFR-BR is a deterministic benchmark framework for evaluating **stateful recovery policies under bounded hardware constraints**.

It models how AI agents behave when recovering from latent state corruption while operating under strict compute and memory budgets.

The framework extends beyond simple recovery testing and introduces:

- Stability phase diagrams
- Differential stability comparison (Cheap vs Robust)
- Empirical collapse boundary extraction
- Theoretical stability inequality validation

SFR-BR formalizes when robustness enlarges the stability region — and when bounded compute induces collapse.

---

# 2. Problem Definition

Modern AI systems assume:

- Infinite compute
- Instant detection
- Unlimited recomputation

In reality:

- Compute is capped
- Memory is bounded
- Detection is delayed
- Recovery consumes resources

This raises a systems question:

> Under bounded compute, does robustness enlarge stability — or destabilize the system?

SFR-BR answers this through deterministic experimentation.

---

# 3. System Architecture

The framework consists of four layers:

---

## 3.1 Agent Layer

Implements recovery policies:

- `BaseAgent` (Cheap strategy)
- `RobustAgent` (Expanded recovery strategy)

Agents receive:

- Current state
- CostState (remaining budget awareness)

Agents output deterministic `Action` objects.

---

## 3.2 Harness Layer

Core execution engine:

- `RecoveryExecutor`
- `CostSimulator`
- `HardwareConstraintVector (HCV)`
- `CostState`
- `Snapshot`

Responsibilities:

- Budget enforcement
- Hard cap detection
- KV recompute charging
- Deterministic execution

---

## 3.3 Failure Model

Latent corruption model:

- KV cache poisoning
- No immediate detection
- Deterministic detection delay
- Recompute cost charged on detection

Detection lag is explicitly modeled via:

```
maybe_detect(detection_probability)
```

---

## 3.4 Stability Classification

Each experiment grid point is classified as:

- Stable (recovery succeeds within cap)
- HardCap Failure (budget exhausted)

This classification enables phase analysis.

---

# 4. Stability Phase Framework

We sweep across:

- Context Depth (D)
- Hard Cost Cap (C)

Each (D, C) pair is evaluated deterministically.

Outputs:

- Stability surface (per agent)
- Differential stability map
- Empirical boundary curves

---

## 4.1 Stability Surface

For each agent:

```
Depth × Cap → Stable / Collapse
```

Produces a phase diagram showing collapse regions.

---

## 4.2 Differential Stability Map

Compares Cheap vs Robust:

- Green → Robust expands stability
- Red → Robust shrinks stability
- Gray → Equal stability

This identifies crossover regions.

---

## 4.3 Stability Boundary Extraction

For each cap:

```
Max Stable Depth
```

Produces empirical collapse curves.

---

# 5. Theoretical Stability Condition

We derive a sufficient stability inequality:

```
c_a · D + k · (D + 1/p) · log(D + 1/p) < C
```

Where:

- D = Context depth
- C = Hard cost cap
- c_a = Action cost coefficient
- k = KV recompute coefficient
- p = Detection probability

A numerical solver estimates theoretical collapse depth.

Empirical boundaries are compared against predicted collapse depth.

---

# 6. Experimental Results

Final stability sweep:

- Total grid points: 56
- Cheap stable points: 6
- Robust stable points: 32
- Cheap stability ratio: 10.7%
- Robust stability ratio: 57.1%
- Net stability expansion: +26 regions

Key finding:

Robustness significantly enlarges the stability region under bounded compute in this configuration.

---

# 7. Determinism & Reproducibility

SFR-BR ensures:

- Deterministic detection delay
- Explicit hardware cap enforcement
- Fixed experiment grids
- No external API calls
- Fully replayable execution

All figures are reproducible via:

```
python main.py
```

---

# 8. Development Evolution (12 Structured Sprints)

SFR-BR evolved through structured iterations:

1. Deterministic executor
2. Hardware constraint modeling
3. Cost simulation integration
4. Latent KV corruption model
5. Detection lag modeling
6. Collapse boundary sweeps
7. Context phase transition mapping
8. Differential stability comparison
9. Formal stability metric extraction
10. Boundary curve extraction
11. Theoretical inequality derivation
12. Empirical-theoretical validation overlay

These iterations refined the system into a coherent stability benchmark.

---

# 9. Project Identity

SFR-BR is:

- A benchmark for stateful recovery under bounded compute
- A deterministic systems framework
- A stability phase analysis engine
- A theoretical + empirical validation artifact

It is not merely a recovery simulator.

It is a stability mapping system for bounded AI recovery.

---

# 10. Conclusion

SFR-BR formalizes:

- When recovery policies remain stable
- When bounded compute induces collapse
- How robustness shifts stability boundaries
- How empirical boundaries compare to theoretical predictions

It provides a reproducible foundation for studying stability under constrained recovery.

---





