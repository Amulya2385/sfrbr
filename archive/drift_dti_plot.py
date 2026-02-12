import matplotlib.pyplot as plt


def plot_drift_dti(dti):
    plt.figure()
    plt.bar(["Drift-Induced DtI"], [dti if dti is not None else 0])
    plt.ylabel("Steps to Detection")
    plt.title("Detection Lag under Gradual Semantic Drift")

    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.1)
    plt.close()
