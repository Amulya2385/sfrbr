# plots/detection_phase_plot.py
# Sprint 8.4.3 — Detection Lag Phase Diagram

import matplotlib.pyplot as plt


def plot_detection_phase(results):
    """
    Plots detection probability vs:
    - Total cost
    - KV depth
    """

    probs = [r["detection_prob"] for r in results]
    costs = [r["cost"] for r in results]
    depths = [r["depth"] for r in results]

    plt.figure()

    plt.plot(probs, costs)
    plt.xlabel("Detection Probability")
    plt.ylabel("Recovery Cost")
    plt.title("Detection Lag Phase Diagram — Cost")

    plt.show(block=False)

    plt.figure()

    plt.plot(probs, depths)
    plt.xlabel("Detection Probability")
    plt.ylabel("KV Depth")
    plt.title("Detection Lag Phase Diagram — Depth")

    plt.show(block=False)
