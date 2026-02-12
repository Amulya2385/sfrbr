# plots/agent_timeline.py
import matplotlib.pyplot as plt


def plot_clean_vs_failure(clean_trace, failure_trace, t_inject, drift_length=None, dti=None):
    clean_y = [a.action_type.value for a in clean_trace]
    fail_y = [a.action_type.value for a in failure_trace]

    plt.figure(figsize=(8, 4))

    plt.plot(clean_y, label="Clean trajectory", marker="o")
    plt.plot(range(t_inject, t_inject + len(fail_y)), fail_y,
             label="Failure / Recovery trajectory", marker="x")

    plt.axvline(t_inject, linestyle="--", color="red", label="Failure Injected")

    if dti is not None:
        plt.axvline(t_inject + dti, linestyle=":", color="purple", label="Detection (DtI)")

    plt.xlabel("Execution Step")
    plt.ylabel("Action Class ID")
    plt.title("Agent Behavior Timeline (Clean vs Failure)")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("plots/agent_timeline.png", dpi=300)
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()



