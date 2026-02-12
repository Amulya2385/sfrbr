# plots/plot_style.py
# Publication-grade matplotlib styling

import matplotlib.pyplot as plt

def apply_publication_style():

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "axes.grid": False,
        "grid.alpha": 0.2,
        "lines.linewidth": 2,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
