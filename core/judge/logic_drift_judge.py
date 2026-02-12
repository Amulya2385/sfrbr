# judge/logic_drift_judge.py

from core.judge.invariants.memory_invariant import MemoryInvariant
from core.judge.invariants.goal_invariant import GoalInvariant


class LogicDriftJudge:
    """
    Sprint 4.5 — Deterministic semantic judge
    """

    def __init__(self):
        self.invariants = [
            MemoryInvariant(),
            GoalInvariant(),
        ]

    def compare(self, clean_state, current_state) -> str:
        for invariant in self.invariants:
            if not invariant.holds(clean_state, current_state):
                return "DIVERGENT"
        return "CONSISTENT"

