# plots/fdi_plot.py
import matplotlib.pyplot as plt


def plot_fdi(clean_throughput, failure_throughput):
    fdi = (
        (clean_throughput - failure_throughput) / clean_throughput
        if clean_throughput > 0 else 0
    )

    plt.figure(figsize=(5, 4))

    labels = ["Clean Fleet", "Failure Fleet"]
    values = [clean_throughput, failure_throughput]
    colors = ["green", "red"]

    bars = plt.bar(labels, values, color=colors)

    for bar in bars:
        h = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, h + 0.2,
                 f"{int(h)}", ha="center")

    plt.text(0.5, max(values) * 0.85, f"FDI = {round(fdi, 2)}",
             ha="center", bbox=dict(boxstyle="round", facecolor="white"))

    plt.ylabel("Throughput")
    plt.title("Fleet Damage Index")
    plt.grid(axis="y", alpha=0.4)

    plt.tight_layout()
    plt.savefig("plots/fdi.png", dpi=300)
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()

