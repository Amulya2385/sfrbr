# experiments/detection_sweep.py
# Sprint 8.4.3 — Detection Lag Phase Diagram (Lower Cap Experiment)

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


def run_detection_sweep():
    """
    Sweeps detection probability under tight hardware cap
    to observe collapse boundary.
    """

    detection_grid = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8]

    results = []

    for dp in detection_grid:

        # 🔥 Lower hardware cap to induce collapse
        hcv = HardwareConstraintVector(
            vram_limit=80,
            kv_eviction_cost=5,
            batch_fragmentation_penalty=10,
            rate_limit_penalty=20,
            hard_cost_cap=900   # ← LOWER CAP EXPERIMENT
        )

        cost_sim = CostSimulator(hcv)

        # Clean reference execution
        clean_agent = RobustAgent()
        exec_clean = Executor(clean_agent, initial_state())

        snapshot = None
        steps = 80

        for t in range(steps):
            if t == 1:
                snapshot = Snapshot(exec_clean.state)
            exec_clean.step()

        # Latent KV poisoning with variable detection probability
        failure_schedule = SilentFailureInjector.latent_kv_poisoning(
            start_step=1,
            token_start=0,
            token_end=32,
            detection_probability=dp
        )

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
            pass

        results.append({
            "detection_prob": dp,
            "depth": executor.state.kv_cache.depth(),
            "cost": cost_sim.total_cost,
            "hard_cap": executor.failed_due_to_hard_cap
        })

    return results

