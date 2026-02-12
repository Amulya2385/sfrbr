# plots/pareto.py
import matplotlib.pyplot as plt


def plot_success_cost(agent_cost, agent_success, ref_cost):
    plt.figure(figsize=(5, 4))

    y = 1 if agent_success else 0
    color = "green" if agent_success else "red"

    plt.scatter(agent_cost, y, s=120, color=color, label="Evaluated Agent")
    plt.scatter(ref_cost, 0, s=120, color="black", marker="x", label="Restart Baseline")

    plt.yticks([0, 1], ["Failure", "Success"])
    plt.xlabel("Recovery Cost")
    plt.title("Success–Cost Pareto Point")
    plt.legend()
    plt.grid(alpha=0.4)

    plt.tight_layout()
    plt.savefig("plots/pareto.png", dpi=300)
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()


