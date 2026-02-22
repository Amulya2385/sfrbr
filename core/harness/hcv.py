# core/harness/hcv.py
# Hardware Constraint Vector — Asymmetric Compute Model

class HardwareConstraintVector:

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

    # -------------------------------------------------
    # Core Action Cost Model (Asymmetric)
    # -------------------------------------------------
    def action_cost(self, action):

        # Base infrastructure cost
        base_cost = self.rate_limit_penalty

        # -------------------------------------------------
        # Structural Asymmetry:
        # Recovery actions cost more infrastructure
        # -------------------------------------------------
        action_name = getattr(action, "type", None)

        if action_name is not None:

            action_str = str(action_name)

            # Penalize recovery-like actions
            if "RECOVERY" in action_str or "ROLLBACK" in action_str:
                base_cost += 2 * self.kv_eviction_cost

            # Penalize memory rebuild
            if "RECOMPUTE" in action_str:
                base_cost += self.kv_eviction_cost

        return base_cost