# results/plots_from_results.py
# Paper-quality plots from your exact results.json structure

import json
import os
import matplotlib.pyplot as plt


RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "plots")


def load_results():
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)


def split_results(results):
    """
    Splits flat list into:
    - agent rows
    - fleet row
    """
    agents = []
    fleet = None

    for entry in results:
        if entry["agent_name"] == "FLEET":
            fleet = entry
        else:
            agents.append(entry)

    return agents, fleet


# ---------------------------------
# Plot 1 — Agent Recovery Cost
# ---------------------------------
def plot_agent_cost(agents):
    labels = [a["agent_name"] for a in agents]
    costs = [a["recovery_cost"] for a in agents]

    plt.figure()
    plt.bar(labels, costs)
    plt.title("Agent Recovery Cost")
    plt.ylabel("Cost")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, "paper_agent_cost.png")
    plt.savefig(output_path)
    print("Saved:", output_path)


# ---------------------------------
# Plot 2 — Agent Recovery Success
# ---------------------------------
def plot_agent_success(agents):
    labels = [a["agent_name"] for a in agents]
    success_vals = [1 if a["recovery_success"] else 0 for a in agents]

    plt.figure()
    plt.bar(labels, success_vals)
    plt.title("Agent Recovery Success (1=True)")
    plt.ylabel("Success")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, "paper_agent_success.png")
    plt.savefig(output_path)
    print("Saved:", output_path)


# ---------------------------------
# Plot 3 — Fleet SRV
# ---------------------------------
def plot_srv(fleet):
    if fleet is None:
        print("No fleet data found.")
        return

    srv_value = fleet["srv"]

    plt.figure()
    plt.bar(["Fleet SRV"], [srv_value])
    plt.title("Systemic Recovery Volatility (SRV)")
    plt.ylabel("SRV")
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, "paper_srv.png")
    plt.savefig(output_path)
    print("Saved:", output_path)


def main():
    results = load_results()
    agents, fleet = split_results(results)

    plot_agent_cost(agents)
    plot_agent_success(agents)
    plot_srv(fleet)


if __name__ == "__main__":
    main()
