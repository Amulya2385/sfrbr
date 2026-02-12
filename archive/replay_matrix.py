# experiments/replay_matrix.py
# Sprint 6.2 — Multi-HCV Counterfactual Replay Matrix

from copy import deepcopy

from core.harness.replay_executor import ReplayExecutor
from core.harness.hcv import HardwareConstraintVector
from core.harness.cost_simulator import CostSimulator


def run_replay_matrix(clean_state, recovery_trace):
    """
    Replays the SAME recovery trace under different hardware envelopes.
    """

    hcv_profiles = {
        "baseline": HardwareConstraintVector(
            vram_limit=80,
            kv_eviction_cost=5,
            batch_fragmentation_penalty=10,
            rate_limit_penalty=20,
            hard_cost_cap=100,
        ),

        "tight_gpu": HardwareConstraintVector(
            vram_limit=40,
            kv_eviction_cost=5,
            batch_fragmentation_penalty=10,
            rate_limit_penalty=20,
            hard_cost_cap=20,   # 🔴 aggressive cap
        ),

        "kv_pressure": HardwareConstraintVector(
            vram_limit=80,
            kv_eviction_cost=20,   # 🔴 expensive recompute
            batch_fragmentation_penalty=10,
            rate_limit_penalty=20,
            hard_cost_cap=100,
        ),
    }

    results = {}

    for name, hcv in hcv_profiles.items():
        state_copy = deepcopy(clean_state)
        cost_sim = CostSimulator(hcv)

        replay = ReplayExecutor(
            state=state_copy,
            action_trace=recovery_trace,
            cost_simulator=cost_sim
        )

        outcome = replay.run()

        results[name] = {
            "success": outcome["success"],
            "total_cost": outcome["total_cost"],
            "hard_cap": hcv.hard_cost_cap,
        }

    return results
