import matplotlib.pyplot as plt


def plot_context_phase(results):

    depths = [r["depth"] for r in results]
    costs = [r["cost"] for r in results]
    hard_caps = [r["hard_cap"] for r in results]

    plt.figure()

    plt.plot(depths, costs, marker="o")
    plt.xlabel("Context Depth (Tokens)")
    plt.ylabel("Recovery Cost")
    plt.title("Context Depth vs Recovery Cost")

    for i, cap in enumerate(hard_caps):
        if cap:
            plt.scatter(depths[i], costs[i])

    plt.show()
