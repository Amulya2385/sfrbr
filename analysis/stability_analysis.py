# experiments/stability_analysis.py
# Formal Stability Region Extraction
# Produces numeric metrics for publication-grade reporting


def extract_stability_metrics(results):

    cheap = results["Cheap"]
    robust = results["Robust"]

    keys = list(cheap.keys())
    total_points = len(keys)

    cheap_stable = 0
    robust_stable = 0

    robust_expansion = 0
    robust_shrink = 0

    crossover_points = []

    for key in keys:

        cheap_outcome = cheap[key]
        robust_outcome = robust[key]

        cheap_is_stable = cheap_outcome == "STABLE"
        robust_is_stable = robust_outcome == "STABLE"

        if cheap_is_stable:
            cheap_stable += 1

        if robust_is_stable:
            robust_stable += 1

        # Differential region analysis
        if robust_is_stable and not cheap_is_stable:
            robust_expansion += 1
            crossover_points.append(
                (key, "ROBUST_EXPANDS")
            )

        elif cheap_is_stable and not robust_is_stable:
            robust_shrink += 1
            crossover_points.append(
                (key, "ROBUST_SHRINKS")
            )

    metrics = {
        "total_grid_points": total_points,
        "cheap_stable_points": cheap_stable,
        "robust_stable_points": robust_stable,
        "cheap_stability_ratio": cheap_stable / total_points,
        "robust_stability_ratio": robust_stable / total_points,
        "robust_expansion_points": robust_expansion,
        "robust_shrink_points": robust_shrink,
        "net_stability_gain": robust_stable - cheap_stable,
        "crossover_points": crossover_points,
    }

    return metrics
