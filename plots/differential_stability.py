# plots/differential_stability.py

import matplotlib.pyplot as plt
import numpy as np
import os


def plot_differential_stability(results):
    """
    results format:
    {
        "Cheap": [(depth, cap), ...],
        "Robust": [(depth, cap), ...]
    }

    Each tuple represents a STABLE point.
    """

    os.makedirs("figures", exist_ok=True)

    cheap_points = set(results["Cheap"])
    robust_points = set(results["Robust"])

    # Union of all grid coordinates
    all_points = cheap_points.union(robust_points)

    if not all_points:
        print("No stability points found.")
        return

    depths = sorted(set(p[0] for p in all_points))
    caps = sorted(set(p[1] for p in all_points))

    depth_index = {d: i for i, d in enumerate(depths)}
    cap_index = {c: i for i, c in enumerate(caps)}

    grid = np.zeros((len(caps), len(depths)))

    for depth, cap in all_points:

        i = cap_index[cap]
        j = depth_index[depth]

        cheap_stable = (depth, cap) in cheap_points
        robust_stable = (depth, cap) in robust_points

        if robust_stable and not cheap_stable:
            grid[i][j] = 1      # Robust expands region
        elif cheap_stable and not robust_stable:
            grid[i][j] = -1     # Robust shrinks region
        elif robust_stable and cheap_stable:
            grid[i][j] = 0.5    # Both stable
        else:
            grid[i][j] = 0      # Both unstable

    plt.figure(figsize=(8, 6))

    plt.imshow(
        grid,
        origin="lower",
        aspect="auto",
        extent=[min(depths), max(depths), min(caps), max(caps)],
        cmap="coolwarm"
    )

    plt.xlabel("Context Depth")
    plt.ylabel("Hard Cost Cap")
    plt.title("Differential Stability Map (Robust vs Cheap)")

    plt.colorbar(label="Stability Difference")

    plt.tight_layout()

    plt.savefig("figures/differential_stability.png", dpi=300)
    plt.savefig("figures/differential_stability.pdf")

    plt.close()


