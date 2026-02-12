import matplotlib.pyplot as plt


def plot_instant_vs_drift(
    clean_trace,
    instant_trace,
    drift_trace,
    t_inject,
    instant_dti,
    drift_dti
):
    """
    Compares agent behavior under instant failure vs gradual drift.
    """

    def encode(trace):
        return [action.action_type.value for action in trace]

    clean_encoded = encode(clean_trace)
    instant_encoded = encode(instant_trace)
    drift_encoded = encode(drift_trace)

    clean_steps = list(range(len(clean_encoded)))
    instant_steps = list(range(t_inject, t_inject + len(instant_encoded)))
    drift_steps = list(range(t_inject, t_inject + len(drift_encoded)))

    plt.figure(figsize=(10, 5))

    # Clean baseline
    plt.plot(
        clean_steps,
        clean_encoded,
        linestyle="-",
        marker="o",
        label="Clean Execution"
    )

    # Instant failure
    plt.plot(
        instant_steps,
        instant_encoded,
        linestyle="--",
        marker="x",
        label=f"Instant Failure (DtI={instant_dti})"
    )

    # Gradual drift
    plt.plot(
        drift_steps,
        drift_encoded,
        linestyle=":",
        marker="s",
        label=f"Gradual Drift (DtI={drift_dti})"
    )

    # Injection marker
    plt.axvline(
        x=t_inject,
        linestyle=":",
        linewidth=2,
        label="Failure Injection"
    )

    plt.xlabel("Execution Step")
    plt.ylabel("Action Class ID")
    plt.title("Instant Failure vs Gradual Semantic Drift")
    plt.legend()
    plt.grid(alpha=0.5)
    plt.tight_layout()

    plt.savefig("plots/instant_vs_drift_timeline.png", dpi=300)

    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
