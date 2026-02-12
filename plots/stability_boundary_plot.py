# plots/stability_boundary_plot.py

import matplotlib.pyplot as plt
from plots.plot_style import apply_publication_style

def plot_stability_boundary(boundary, theoretical=None):

    apply_publication_style()

    caps = sorted(boundary["Cheap"].keys())

    cheap_depths = [boundary["Cheap"][c] for c in caps]
    robust_depths = [boundary["Robust"][c] for c in caps]

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.plot(caps, cheap_depths, marker="o", label="Cheap Empirical")
    ax.plot(caps, robust_depths, marker="s", label="Robust Empirical")

    if theoretical:
        theo_depths = [theoretical[c] for c in caps]
        ax.plot(caps, theo_depths, linestyle="--", label="Theoretical Bound")

    ax.set_title("Stability Boundary: Empirical vs Theoretical")
    ax.set_xlabel("Hard Cost Cap")
    ax.set_ylabel("Max Stable Depth")

    ax.legend()

    plt.tight_layout()

    plt.savefig("figures/stability_boundary.png")
    plt.savefig("figures/stability_boundary.pdf")

    plt.show()

