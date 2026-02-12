# judge/base_judge.py

class BaseSemanticJudge:
    """
    Abstract base class for all semantic judges.

    Judges MUST be:
    - Deterministic
    - Binary (EQUIVALENT / DIVERGENT)
    - Auditable
    """

    def compare(self, clean_state, current_state):
        """
        Compare two states and return:
        - "EQUIVALENT"
        - "DIVERGENT"
        """
        raise NotImplementedError

