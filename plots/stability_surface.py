# plots/stability_surface.py

import matplotlib.pyplot as plt
import numpy as np
import os


def plot_stability_surface(results, agent_name):

    """
    results format:
    {
        "Cheap": [(depth, cap), ...],
        "Robust": [(depth, cap), ...]
    }

    Each tuple represents a STABLE point.
    """

    os.makedirs("figures", exist_ok=True)

    agent_results = results[agent_name]

    if not agent_results:
        print(f"No stable points for {agent_name}")
        return

    # Extract unique axes
    depths = sorted(set(r[0] for r in agent_results))
    caps = sorted(set(r[1] for r in agent_results))

    depth_index = {d: i for i, d in enumerate(depths)}
    cap_index = {c: i for i, c in enumerate(caps)}

    grid = np.zeros((len(caps), len(depths)))

    # Mark stable points as 1
    for depth, cap in agent_results:
        i = cap_index[cap]
        j = depth_index[depth]
        grid[i][j] = 1

    plt.figure(figsize=(8, 6))

    plt.imshow(
        grid,
        origin="lower",
        aspect="auto",
        extent=[min(depths), max(depths), min(caps), max(caps)]
    )

    plt.xlabel("Context Depth")
    plt.ylabel("Hard Cost Cap")
    plt.title(f"Stability Phase Diagram — {agent_name} Agent")

    plt.colorbar(label="Stable Region")

    plt.tight_layout()

    plt.savefig(f"figures/stability_surface_{agent_name}.png", dpi=300)
    plt.savefig(f"figures/stability_surface_{agent_name}.pdf")

    plt.close()


