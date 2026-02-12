# harness/cost_state.py
# Sprint 8 — Elastic Budget Signal (FINAL)

class CostState:
    """
    Read-only cost visibility for agents.
    Deterministic and auditable.
    """

    def __init__(self, total_cost, hard_cap, last_action_cost=0.0):
        self.total_cost = total_cost
        self.hard_cap = hard_cap
        self.last_action_cost = last_action_cost

        if hard_cap and hard_cap > 0:
            ratio = total_cost / hard_cap
        else:
            ratio = 0.0

        # Expose BOTH names for safety & compatibility
        self.used_ratio = ratio
        self.used_budget_ratio = ratio  # <- matches RobustAgent

    def nearing_cap(self):
        return self.used_budget_ratio >= 0.7

    def critical(self):
        return self.used_budget_ratio >= 0.9

    def __repr__(self):
        return (
            f"CostState(total={self.total_cost}, "
            f"ratio={self.used_budget_ratio:.2f}, "
            f"last={self.last_action_cost})"
        )

