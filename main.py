# ============================================================
# SFR-BR — Stability Failure Recovery under Bounded Resources
# Final Publication Entry Point
# ============================================================

import os

# Ensure figure directory exists
os.makedirs("figures", exist_ok=True)

# ============================================================
# IMPORTS
# ============================================================

# Experiments
from experiments.stability_phase import run_stability_phase
from experiments.stability_boundary import extract_stability_boundary

# Analysis
from analysis.stability_analysis import extract_stability_metrics
from analysis.theoretical_boundary_solver import generate_theoretical_boundary

# Plots
from plots.plot_style import apply_publication_style
from plots.stability_surface import plot_stability_surface
from plots.differential_stability import plot_differential_stability
from plots.stability_boundary_plot import plot_stability_boundary


# ============================================================
# APPLY GLOBAL PUBLICATION STYLE
# ============================================================

apply_publication_style()


# ============================================================
# 1️⃣ RUN STABILITY PHASE EXPERIMENT
# ============================================================

print("\n=== RUNNING STABILITY PHASE EXPERIMENT ===")

stability_results = run_stability_phase()


# ============================================================
# 2️⃣ STABILITY SURFACE — ROBUST
# ============================================================

print("Generating Stability Surface (Robust)...")

plot_stability_surface(
    stability_results,
    agent_name="Robust"
)


# ============================================================
# 3️⃣ STABILITY SURFACE — CHEAP
# ============================================================

print("Generating Stability Surface (Cheap)...")

plot_stability_surface(
    stability_results,
    agent_name="Cheap"
)


# ============================================================
# 4️⃣ DIFFERENTIAL STABILITY MAP
# ============================================================

print("Generating Differential Stability Map...")

plot_differential_stability(stability_results)


# ============================================================
# 5️⃣ EXTRACT EMPIRICAL BOUNDARIES
# ============================================================

print("Extracting Empirical Stability Boundaries...")

boundary = extract_stability_boundary(stability_results)


# ============================================================
# 6️⃣ COMPUTE THEORETICAL BOUNDARY
# ============================================================

print("Computing Theoretical Boundary...")

caps = sorted(boundary["Cheap"].keys())

# System parameters aligned with experiment
c_a = 20   # rate_limit_penalty
k = 5      # kv_eviction_cost
p = 0.3    # detection probability

theoretical_boundary = generate_theoretical_boundary(
    caps=caps,
    c_a=c_a,
    k=k,
    p=p,
    max_search_depth=5000
)


# ============================================================
# 7️⃣ PLOT EMPIRICAL + THEORY OVERLAY
# ============================================================

print("Generating Boundary Comparison Plot...")

plot_stability_boundary(
    boundary,
    theoretical=theoretical_boundary
)


# ============================================================
# 8️⃣ PRINT FINAL METRICS
# ============================================================

print("\n=== FINAL STABILITY METRICS ===")

metrics = extract_stability_metrics(stability_results)

for key, value in metrics.items():
    if key != "crossover_points":
        print(f"{key}: {value}")

print("\nCrossover Points:")
for point in metrics["crossover_points"]:
    print(point)


print("\nSFR-BR Final Stability Analysis Complete.")
# ============================================
# ULTRA-TIGHT CAP INVERSION SEARCH
# ============================================

from experiments.stability_inversion import run_inversion_sweep

run_inversion_sweep()









