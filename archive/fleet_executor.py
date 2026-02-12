# experiments/fleet_executor.py
# Sprint 8.3 — Aggressive Collapse Model (Convex SRV)
# Deterministic non-linear infrastructure stress

from core.harness.recovery_executor import RecoveryExecutor
from core.harness.cost_simulator import CostSimulator


class FleetExecutor:
    """
    Simulates multiple agents recovering simultaneously.

    Implements convex SRV collapse model:
        SRV = α * (rollback_count^2)
            + β * (prefix_break_ratio^2)

    Deterministic and reproducible.
    """

    def __init__(self, agents, state_factory, budget_factory, hcv):
        self.agents = agents
        self.state_factory = state_factory
        self.budget_factory = budget_factory
        self.hcv = hcv

        self.executors = []
        self.systemic_penalty = 0.0
        self.fleet_steps = 0

        # Convex coefficients (Aggressive Mode)
        self.alpha = 5.0     # rollback impact
        self.beta = 100.0    # prefix collapse impact

    # --------------------------------------------------
    # Initialize fleet
    # --------------------------------------------------
    def _initialize(self):
        self.executors = []

        for agent in self.agents:
            state = self.state_factory()
            budget = self.budget_factory()
            cost_sim = CostSimulator(self.hcv)

            executor = RecoveryExecutor(
                agent=agent,
                state=state,
                budget=budget,
                cost_simulator=cost_sim,
                semantic_judge=None,
                clean_snapshot=None,
            )

            self.executors.append(executor)

    # --------------------------------------------------
    # Run Fleet
    # --------------------------------------------------
    def run(self, max_steps=10):

        self._initialize()

        for step in range(max_steps):

            rollback_count = 0
            active_agents = 0

            for executor in self.executors:
                try:
                    action = executor.step()
                    active_agents += 1

                    if action.action_type.name == "ROLLBACK":
                        rollback_count += 1

                except RuntimeError:
                    # Agent died due to hard cap or divergence
                    continue

            # ----------------------------
            # Convex Collapse Model
            # ----------------------------

            if active_agents > 0:

                prefix_break_ratio = rollback_count / active_agents

                srv_increment = (
                    self.alpha * (rollback_count ** 2)
                    + self.beta * (prefix_break_ratio ** 2)
                )

                self.systemic_penalty += srv_increment

            self.fleet_steps += 1

        return {
            "systemic_penalty": self.systemic_penalty,
            "fleet_steps": self.fleet_steps,
            "agent_count": len(self.agents),
        }
