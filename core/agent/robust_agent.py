# agent/robust_agent.py
# Sprint 8.5 — Behavioral Coupling

from core.agent.actions import Action, ActionType


class RobustAgent:
    """
    Robust agent with infrastructure-aware behavioral coupling.

    Modes:
    - Clean Mode
    - Latent Corruption Mode (undetected)
    - Detected Corruption Mode (defensive containment)
    - Budget-Aware Mode (elastic degradation)
    """

    def act(self, state, cost_state=None):

        kv = getattr(state, "kv_cache", None)

        # -----------------------------
        # 1️⃣ Budget-aware degradation
        # -----------------------------
        if cost_state and cost_state.used_budget_ratio > 0.9:
            # Near hard cap → freeze expansion
            return Action(ActionType.NOOP)

        # -----------------------------
        # 2️⃣ If KV exists
        # -----------------------------
        if kv:

            # Clean Mode
            if not kv.poisoned:
                return Action(ActionType.PLAN_EXPAND)

            # Latent Corruption (not yet detected)
            if kv.poisoned and not kv.detected:
                # Overconfident expansion → future collapse
                return Action(ActionType.PLAN_EXPAND)

            # Detected Corruption
            if kv.poisoned and kv.detected:
                # Defensive containment mode
                # Avoid expansion explosion
                return Action(ActionType.MEMORY_READ)

        # Fallback
        return Action(ActionType.PLAN_EXPAND)

