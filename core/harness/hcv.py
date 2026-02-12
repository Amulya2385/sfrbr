# harness/hcv.py
# Hardware Constraint Vector (HCV)
# Sprint 5: Physical, action-driven cost model

from core.agent.actions import ActionType


class HardwareConstraintVector:
    """
    Deterministic hardware cost model.
    Maps actions → physical system penalties.
    """

    def __init__(
        self,
        vram_limit,
        kv_eviction_cost,
        batch_fragmentation_penalty,
        rate_limit_penalty,
        hard_cost_cap=None,
    ):
        self.vram_limit = vram_limit
        self.kv_eviction_cost = kv_eviction_cost
        self.batch_fragmentation_penalty = batch_fragmentation_penalty
        self.rate_limit_penalty = rate_limit_penalty
        self.hard_cost_cap = hard_cost_cap

    def action_cost(self, action):
        """
        Sprint 5 semantics:
        Action → REAL infra cost
        """

        if action.action_type == ActionType.PLAN_EXPAND:
            # KV growth + eviction pressure
            return self.kv_eviction_cost * 3

        if action.action_type == ActionType.ROLLBACK:
            # Prefix recompute + batch fragmentation
            return (
                self.kv_eviction_cost * 5 +
                self.batch_fragmentation_penalty * 3
            )

        if action.action_type == ActionType.TOOL_CALL:
            return self.rate_limit_penalty * 2

        if action.action_type == ActionType.MEMORY_WRITE:
            return 1.0

        if action.action_type == ActionType.MEMORY_READ:
            return 0.2

        if action.action_type == ActionType.NOOP:
            return 0.0

        return 0.0



