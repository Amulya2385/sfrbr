# plots/srv_plot.py

import matplotlib.pyplot as plt


def plot_srv(srv_value, agent_count):
    """
    Visualizes Systemic Recovery Volatility (SRV)
    as total external penalty imposed on the fleet.
    """

    plt.figure()
    plt.bar(
        ["Fleet SRV"],
        [srv_value]
    )

    plt.ylabel("Systemic Penalty (Cost Units)")
    plt.title(
        f"Systemic Recovery Volatility (SRV)\n"
        f"{agent_count} Agents, Shared Hardware"
    )

    plt.tight_layout()
    plt.show()
