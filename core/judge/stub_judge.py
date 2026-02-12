# judge/stub_judge.py
from core.judge.base_judge import BaseSemanticJudge


class StubSemanticJudge(BaseSemanticJudge):
    """
    Deterministic no-op judge.
    Always returns EQUIVALENT.
    """

    def compare(self, clean_state, current_state):
        return "EQUIVALENT"

