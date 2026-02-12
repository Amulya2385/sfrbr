import matplotlib.pyplot as plt


def plot_future_probes(probe_details):
    """
    Visualizes post-recovery probe outcomes.
    Bars always appear; color encodes PASS / FAIL.
    """

    labels = []
    colors = []
    annotations = []

    for key, result in probe_details.items():
        if isinstance(result, bool):
            labels.append(key.replace("_", " ").title())
            colors.append("green" if result else "red")
            annotations.append("PASS" if result else "FAIL")

    if not labels:
        return  # nothing to plot

    values = [1] * len(labels)  # constant height so bars are visible

    plt.figure(figsize=(6, 3))
    bars = plt.bar(labels, values, color=colors)

    for bar, text in zip(bars, annotations):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            0.5,
            text,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            color="white"
        )

    plt.ylim(0, 1.2)
    plt.ylabel("Probe Outcome")
    plt.title("Future Damage Probe Results")
    plt.yticks([])
    plt.tight_layout()

    plt.savefig("plots/future_probe_stability.png", dpi=300)
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()


