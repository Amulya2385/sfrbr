# harness/cost_simulator.py
# Sprint 8.4.2 — Collapse Boundary Model

import math


class CostSimulator:
    def __init__(self, hcv):
        self.hcv = hcv
        self.total_cost = 0.0
        self.last_action_cost = 0.0

    # -----------------------------------
    # Standard action cost
    # -----------------------------------
    def charge(self, action):
        cost = self.hcv.action_cost(action)
        self.total_cost += cost
        self.last_action_cost = cost

    # -----------------------------------
    # KV Recompute (Log-Linear Scaling)
    # -----------------------------------
    def charge_kv_recompute(self, kv_cache):

        tokens = kv_cache.depth()

        if tokens <= 1:
            return

        # 🔥 Log-linear scaling instead of quadratic
        recompute_cost = tokens * math.log(tokens)

        self.total_cost += recompute_cost
        self.last_action_cost = recompute_cost

    # -----------------------------------
    def exceeded_hard_cap(self):
        if self.hcv.hard_cost_cap is None:
            return False
        return self.total_cost > self.hcv.hard_cost_cap

    # -----------------------------------
    def compute_cost(self):
        return self.total_cost











