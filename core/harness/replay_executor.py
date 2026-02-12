# harness/replay_executor.py
# Sprint 6.1 — Counterfactual Replay Executor
# Deterministic, agent-free, physics-only replay

from core.agent.actions import Action


class ReplayExecutor:
    """
    Replays a fixed recovery trace under a new HardwareConstraintVector.
    No agent calls. No failure injection. No nondeterminism.
    """

    def __init__(self, state, action_trace, cost_simulator):
        self.state = state
        self.action_trace = action_trace
        self.cost_simulator = cost_simulator

        self.failed_due_to_hard_cap = False
        self.total_cost = 0.0

    def run(self):
        """
        Replay the trace step-by-step.
        """

        for action in self.action_trace:
            if not isinstance(action, Action):
                raise RuntimeError("Replay trace must contain Action objects")

            # Apply cost
            self.cost_simulator.charge(action)

            if self.cost_simulator.exceeded_hard_cap():
                self.failed_due_to_hard_cap = True
                break

            # Apply state mutation
            action.apply(self.state)

        self.total_cost = self.cost_simulator.total_cost

        return {
            "success": not self.failed_due_to_hard_cap,
            "total_cost": self.total_cost
        }
