# experiments/stability_inversion.py
# Expanded Cap Sweep — Three-Phase Detection

from experiments.stability_phase import run_stability_phase


def run_inversion_sweep():

    print("\n==============================")
    print(" STABILITY INVERSION SEARCH")
    print("==============================")

    detection_probs = [0.1, 0.2, 0.3, 0.5]

    # 🔥 Expanded Cap Range
    cap_grid = list(range(50, 6500, 250))

    depth_grid = [200, 400]

    inversion_found = False

    for p in detection_probs:

        print(f"\n--- Detection Probability: {p} ---")

        for depth in depth_grid:

            print(f"\nTesting Depth: {depth}")

            results = run_stability_phase(
                custom_depths=[depth],
                custom_caps=cap_grid,
                detection_probability=p
            )

            for cap in cap_grid:

                cheap = results["Cheap"][(depth, cap)]
                robust = results["Robust"][(depth, cap)]

                print(
                    f"Cap: {cap} | Cheap: {cheap} | Robust: {robust}"
                )

                # 🔥 Inversion condition
                if cheap == "STABLE" and robust == "INFRASTRUCTURE_COLLAPSE":
                    inversion_found = True
                    print("\n🔥 INVERSION DETECTED 🔥")
                    print(f"Depth: {depth}, Cap: {cap}, p: {p}")

    if not inversion_found:
        print("\nNo inversion detected in evaluated parameter space.")