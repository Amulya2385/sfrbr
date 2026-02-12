# experiments/counterfactual_gate.py
# Sprint 6.3 — Counterfactual Consistency Gate

def counterfactual_gate(replay_results, required_profiles=None):
    """
    Determines whether a recovery strategy is
    counterfactually robust.

    replay_results:
        output of run_replay_matrix()

    required_profiles:
        list of profiles that MUST pass
    """

    if required_profiles is None:
        required_profiles = list(replay_results.keys())

    failures = []

    for profile in required_profiles:
        result = replay_results.get(profile)

        if result is None:
            failures.append((profile, "MISSING"))
        elif not result["success"]:
            failures.append((profile, "FAILED"))

    return {
        "counterfactual_pass": len(failures) == 0,
        "failures": failures
    }
