# experiments/stability_boundary.py
# Stability Boundary Curve Extraction


def extract_stability_boundary(results):

    cheap = results["Cheap"]
    robust = results["Robust"]

    # Collect unique caps and depths
    caps = sorted(set(cap for (_, cap) in cheap.keys()))
    depths = sorted(set(depth for (depth, _) in cheap.keys()))

    cheap_boundary = {}
    robust_boundary = {}

    for cap in caps:

        # For this cap, find maximum stable depth
        cheap_max_depth = 0
        robust_max_depth = 0

        for depth in depths:

            key = (depth, cap)

            if key in cheap:
                if cheap[key] == "STABLE":
                    cheap_max_depth = max(cheap_max_depth, depth)

            if key in robust:
                if robust[key] == "STABLE":
                    robust_max_depth = max(robust_max_depth, depth)

        cheap_boundary[cap] = cheap_max_depth
        robust_boundary[cap] = robust_max_depth

    return {
        "Cheap": cheap_boundary,
        "Robust": robust_boundary
    }
