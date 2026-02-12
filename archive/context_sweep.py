# experiments/context_sweep.py
# Sprint 8.4.1 — Context Phase Transition Sweep (Aggressive Regime)

from core.agent.robust_agent import RobustAgent
from core.harness.executor import Executor
from core.harness.recovery_executor import RecoveryExecutor
from core.harness.failure import SilentFailureInjector
from core.harness.snapshot import Snapshot
from core.harness.budgets import RecoveryBudget
from core.harness.hcv import HardwareConstraintVector
from core.harness.cost_simulator import CostSimulator
from tasks.task_definition import initial_state
from core.judge.logic_drift_judge import LogicDriftJudge


def run_context_sweep():
    """
    Sweeps increasing context depth to observe
    phase transition under bounded hardware.
    """

    # 🔥 Aggressive depth sweep
    step_grid = [20, 40, 80, 120, 160, 200, 240, 280, 320, 360]




    results = []

    for steps in step_grid:

        # -----------------------------
        # Hardware setup (Lower cap)
        # -----------------------------
        hcv = HardwareConstraintVector(
    vram_limit=80,
    kv_eviction_cost=5,
    batch_fragmentation_penalty=10,
    rate_limit_penalty=20,
    hard_cost_cap=5000  # 🔥 Increased for boundary detection
)


        cost_sim = CostSimulator(hcv)

        # -----------------------------
        # Clean reference execution
        # -----------------------------
        clean_agent = RobustAgent()
        exec_clean = Executor(clean_agent, initial_state())

        snapshot = None
        for t in range(steps):
            if t == 1:
                snapshot = Snapshot(exec_clean.state)
            exec_clean.step()

        # -----------------------------
        # Latent KV Poisoning
        # -----------------------------
        failure_schedule = SilentFailureInjector.latent_kv_poisoning(
            start_step=1,
            token_start=0,
            token_end=32,
            detection_probability=0.4  # 🔥 increased detection
        )

        # -----------------------------
        # Recovery executor
        # -----------------------------
        executor = RecoveryExecutor(
            agent=RobustAgent(),
            state=snapshot.restore(),
            budget=RecoveryBudget(max_steps=steps),
            cost_simulator=cost_sim,
            semantic_judge=LogicDriftJudge(),
            clean_snapshot=snapshot
        )

        executor.failure_schedule = failure_schedule

        try:
            for _ in range(steps):
                executor.step()
        except RuntimeError:
            # Collapse is expected at high depth
            pass

        depth = executor.state.kv_cache.depth()
        cost = cost_sim.total_cost
        hard_cap = executor.failed_due_to_hard_cap

        results.append({
            "steps": steps,
            "depth": depth,
            "cost": cost,
            "hard_cap": hard_cap
        })

    return results
