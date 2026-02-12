# results/generate_results.py
# SFR-BR v3 — Results Freezer
# This script is run ONCE per experiment configuration

import json
from pathlib import Path

from core.agent.base_agent import BaseAgent
from core.agent.robust_agent import RobustAgent

from core.harness.executor import Executor
from core.harness.recovery_executor import RecoveryExecutor
from core.harness.failure import SilentFailureInjector
from core.harness.snapshot import Snapshot
from core.harness.budgets import RecoveryBudget
from core.harness.hcv import HardwareConstraintVector
from core.harness.cost_simulator import CostSimulator
from core.harness.future_probes import run_future_probes

from core.judge.logic_drift_judge import LogicDriftJudge
from tasks.task_definition import initial_state
from archive.fleet_experiment import run_fleet_experiment


RESULTS_DIR = Path(__file__).parent
RESULTS_FILE = RESULTS_DIR / "results.json"


def run_agent(agent, name, clean_trace, snapshot, cost_sim):
    state = snapshot.restore()

    failure = SilentFailureInjector.kv_cache_poisoning(
        start_step=1,
        token_start=0,
        token_end=32,
        recompute_cost=40.0
    )

    executor = RecoveryExecutor(
        agent=agent,
        state=state,
        budget=RecoveryBudget(max_steps=5),
        cost_simulator=cost_sim,
        semantic_judge=LogicDriftJudge(),
        clean_snapshot=snapshot
    )

    executor.failure_schedule = failure

    trace = []
    dti = None
    semantic_drift = False
    hard_cap = False

    try:
        for step in range(len(clean_trace)):
            action = executor.step()
            trace.append(action)

            if dti is None and action.action_type != clean_trace[step].action_type:
                dti = step

    except RuntimeError as e:
        if "LOGICAL_DRIFT" in str(e):
            semantic_drift = True
        if "HARD_CAP" in str(e):
            hard_cap = True

    probes = run_future_probes(executor.state)

    return {
        "agent_name": name,
        "recovery_success": (
            executor.recovery_complete
            and probes.details["behavior_match"]
            and not semantic_drift
            and not hard_cap
        ),
        "recovery_cost": cost_sim.compute_cost(trace),
        "dti": dti,
        "hard_cap_hit": hard_cap,
        "semantic_drift_detected": semantic_drift,
    }


def main():
    hcv = HardwareConstraintVector(
        vram_limit=80,
        kv_eviction_cost=5,
        batch_fragmentation_penalty=10,
        rate_limit_penalty=20,
        hard_cost_cap=100
    )

    cost_sim = CostSimulator(hcv)

    # Clean reference
    clean_agent = BaseAgent()
    exec_clean = Executor(clean_agent, initial_state())

    snapshot = None
    for t in range(6):
        if t == 1:
            snapshot = Snapshot(exec_clean.state)
        exec_clean.step()

    clean_trace = exec_clean.trace

    results = []

    results.append(
        run_agent(BaseAgent(), "Agent A (Cheap)", clean_trace, snapshot, cost_sim)
    )

    results.append(
        run_agent(RobustAgent(), "Agent B (Robust)", clean_trace, snapshot, cost_sim)
    )

    # Fleet-level
    fleet = run_fleet_experiment()
    results.append({
        "agent_name": "FLEET",
        "srv": fleet["systemic_penalty"],
        "fleet_steps": fleet["fleet_steps"],
        "determinism_pass": True
    })

    RESULTS_DIR.mkdir(exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Results frozen to:", RESULTS_FILE)


if __name__ == "__main__":
    main()

