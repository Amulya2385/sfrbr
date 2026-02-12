# experiments/stability_phase.py
# FINAL — Stability Phase Diagram Experiment
# Maps stability region under (context_depth × hard_cost_cap)

from core.agent.base_agent import BaseAgent
from core.agent.robust_agent import RobustAgent

from core.harness.executor import Executor
from core.harness.recovery_executor import RecoveryExecutor
from core.harness.failure import SilentFailureInjector
from core.harness.snapshot import Snapshot
from core.harness.budgets import RecoveryBudget
from core.harness.hcv import HardwareConstraintVector
from core.harness.cost_simulator import CostSimulator

from core.judge.logic_drift_judge import LogicDriftJudge
from tasks.task_definition import initial_state


# ---------------------------------------------
# Outcome Labels
# ---------------------------------------------
STABLE = "STABLE"
HARD_CAP = "INFRASTRUCTURE_COLLAPSE"
LOGICAL = "LOGICAL_COLLAPSE"


# ---------------------------------------------
# Single Configuration Run
# ---------------------------------------------
def run_configuration(agent_cls, depth, cap):

    # -----------------------------
    # Hardware setup
    # -----------------------------
    hcv = HardwareConstraintVector(
        vram_limit=80,
        kv_eviction_cost=5,
        batch_fragmentation_penalty=10,
        rate_limit_penalty=20,
        hard_cost_cap=cap,
    )

    cost_sim = CostSimulator(hcv)

    # -----------------------------
    # Clean reference
    # -----------------------------
    clean_agent = agent_cls()
    exec_clean = Executor(clean_agent, initial_state())

    snapshot = None

    for t in range(depth):
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
        detection_probability=0.3,
    )

    # -----------------------------
    # Recovery Executor
    # -----------------------------
    executor = RecoveryExecutor(
        agent=agent_cls(),
        state=snapshot.restore(),
        budget=RecoveryBudget(max_steps=depth),
        cost_simulator=cost_sim,
        semantic_judge=LogicDriftJudge(),
        clean_snapshot=snapshot,
    )

    executor.failure_schedule = failure_schedule

    # -----------------------------
    # Execute
    # -----------------------------
    try:
        for _ in range(depth):
            executor.step()

    except RuntimeError as e:

        if executor.failed_due_to_hard_cap:
            return HARD_CAP

        if "LOGICAL_DRIFT_DETECTED" in str(e):
            return LOGICAL

        return HARD_CAP

    # -----------------------------
    # Stable case
    # -----------------------------
    return STABLE


# ---------------------------------------------
# Stability Phase Sweep
# ---------------------------------------------
def run_stability_phase():

    depth_grid = [50, 100, 200, 400, 800, 1200, 1600, 2000]
    cap_grid = [300, 500, 800, 1200, 2000, 3000, 5000]

    results = {
        "Cheap": {},
        "Robust": {}
    }

    # -----------------------------
    # Cheap Agent
    # -----------------------------
    for depth in depth_grid:
        for cap in cap_grid:
            outcome = run_configuration(BaseAgent, depth, cap)
            results["Cheap"][(depth, cap)] = outcome

    # -----------------------------
    # Robust Agent
    # -----------------------------
    for depth in depth_grid:
        for cap in cap_grid:
            outcome = run_configuration(RobustAgent, depth, cap)
            results["Robust"][(depth, cap)] = outcome

    return results
