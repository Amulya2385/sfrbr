# results/final_tables.py
# SFR-BR v3 — Final Paper Tables

import json
from pathlib import Path

RESULTS_FILE = Path(__file__).parent / "results.json"


def load_results():
    with open(RESULTS_FILE, "r") as f:
        return json.load(f)


def agent_table(results):
    print("\nTABLE 1 — Agent-Level Recovery Performance")
    print("-" * 60)
    print(
        "Agent | Success | Cost | DtI | HardCap | Semantic Drift"
    )
    print("-" * 60)

    for r in results:
        if r["agent_name"] == "FLEET":
            continue

        print(
            f"{r['agent_name']} | "
            f"{r['recovery_success']} | "
            f"{r['recovery_cost']} | "
            f"{r['dti']} | "
            f"{r['hard_cap_hit']} | "
            f"{r['semantic_drift_detected']}"
        )


def fleet_table(results):
    print("\nTABLE 2 — Fleet-Level Impact")
    print("-" * 60)
    print("Metric | Value")
    print("-" * 60)

    for r in results:
        if r["agent_name"] == "FLEET":
            print(f"SRV | {r['srv']}")
            print(f"Determinism | {r['determinism_pass']}")


def main():
    results = load_results()
    agent_table(results)
    fleet_table(results)


if __name__ == "__main__":
    main()
