# judge/logic_invariants.py

class LogicInvariant:
    """
    A deterministic invariant over agent state.
    """

    def check(self, clean_state, current_state) -> bool:
        raise NotImplementedError


class MemoryInvariant(LogicInvariant):
    """
    Memory keys that must not silently change.
    """

    def __init__(self, protected_keys):
        self.protected_keys = protected_keys

    def check(self, clean_state, current_state) -> bool:
        for key in self.protected_keys:
            if clean_state.memory.get(key) != current_state.memory.get(key):
                return False
        return True


class GoalInvariant(LogicInvariant):
    """
    Ensures task goal remains unchanged.
    """

    def check(self, clean_state, current_state) -> bool:
        return clean_state.goal == current_state.goal
