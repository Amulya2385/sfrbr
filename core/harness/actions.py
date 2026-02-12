from enum import Enum, auto


class ActionType(Enum):
    NOOP = auto()
    WRITE = auto()
    PLAN_EXPAND = auto()
    ROLLBACK = auto()


class Action:
    def __init__(self, action_type, payload=None, reasoning=None):
        self.action_type = action_type
        self.payload = payload or {}
        self.reasoning = reasoning

    def apply(self, state):
        """
        Deterministic state transition.
        REQUIRED for v3 (non-simulation).
        """

        if self.action_type == ActionType.NOOP:
            return

        if self.action_type == ActionType.WRITE:
            key = self.payload.get("key")
            value = self.payload.get("value")
            state.memory[key] = value
            return

        if self.action_type == ActionType.PLAN_EXPAND:
            state.plan_depth += 1
            return

        if self.action_type == ActionType.ROLLBACK:
            state.restore_last_snapshot()
            return

        raise RuntimeError(f"Unknown ActionType: {self.action_type}")

