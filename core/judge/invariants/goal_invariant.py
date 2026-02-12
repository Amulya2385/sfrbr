# judge/invariants/goal_invariant.py
# Sprint 4.5 — Goal Invariant

from core.judge.invariants.base_invariant import BaseInvariant


class GoalInvariant(BaseInvariant):
    """
    Ensures agent goal does not drift during recovery.
    """

    def holds(self, clean_state, current_state) -> bool:
        if hasattr(clean_state, "goal") and hasattr(current_state, "goal"):
            return clean_state.goal == current_state.goal

        return True

