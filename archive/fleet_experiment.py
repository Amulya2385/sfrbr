# experiments/fleet_experiment.py
# Sprint 8.3 — Compatible with Convex FleetExecutor

from core.agent.base_agent import BaseAgent
from core.agent.robust_agent import RobustAgent

from core.harness.budgets import RecoveryBudget
from core.harness.hcv import HardwareConstraintVector
from tasks.task_definition import initial_state

from archive.fleet_executor import FleetExecutor


def run_fleet_experiment():

    # -----------------------------
    # Hardware profile
    # -----------------------------
    hcv = HardwareConstraintVector(
        vram_limit=80,
        kv_eviction_cost=5,
        batch_fragmentation_penalty=10,
        rate_limit_penalty=20,
        hard_cost_cap=100,
    )

    # -----------------------------
    # Agent population
    # -----------------------------
    agents = [
        BaseAgent(),
        RobustAgent(),
        BaseAgent(),
        RobustAgent(),
    ]

    # -----------------------------
    # State factory (fresh per agent)
    # -----------------------------
    def state_factory():
        return initial_state()

    # -----------------------------
    # Budget factory (fresh per agent)
    # -----------------------------
    def budget_factory():
        return RecoveryBudget(max_steps=6)

    # -----------------------------
    # Fleet Executor (Sprint 8.3)
    # -----------------------------
    fleet = FleetExecutor(
        agents=agents,
        state_factory=state_factory,
        budget_factory=budget_factory,
        hcv=hcv,
    )

    result = fleet.run(max_steps=10)

    return result




