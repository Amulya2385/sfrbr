# plots/agent_comparison.py
import matplotlib.pyplot as plt


def plot_agent_comparison(results):
    labels = [r["label"] for r in results]
    costs = [r["cost"] for r in results]
    success = [r["success"] for r in results]

    colors = ["green" if s else "red" for s in success]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(labels, costs, color=colors)

    for bar, s in zip(bars, success):
        txt = "VALID" if s else "INVALID"
        plt.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 1,
                 txt, ha="center", fontweight="bold")

    plt.ylabel("Recovery Cost")
    plt.title("Agent Recovery Comparison")
    plt.grid(axis="y", alpha=0.4)

    plt.tight_layout()
    plt.savefig("plots/agent_comparison.png", dpi=300)
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
