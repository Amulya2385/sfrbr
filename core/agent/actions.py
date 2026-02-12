# agent/action.py
from enum import Enum


class ActionType(Enum):
    PLAN_EXPAND = "PLAN_EXPAND"
    MEMORY_READ = "MEMORY_READ"
    MEMORY_WRITE = "MEMORY_WRITE"
    TOOL_CALL = "TOOL_CALL"
    ROLLBACK = "ROLLBACK"
    NOOP = "NOOP"


class Action:
    """
    Deterministic execution unit.
    The ONLY place state is mutated.
    """

    def __init__(self, action_type: ActionType, parameter=None, reasoning=""):
        self.action_type = action_type
        self.parameter = parameter
        self.reasoning = reasoning

    def apply(self, state):
        if self.action_type == ActionType.MEMORY_WRITE:
            # parameter must be (key, value)
            key, value = self.parameter
            state.memory[key] = value

        elif self.action_type == ActionType.MEMORY_READ:
            pass

        elif self.action_type == ActionType.PLAN_EXPAND:
            state.step += 1

        elif self.action_type == ActionType.TOOL_CALL:
            state.tool_calls += 1

        elif self.action_type == ActionType.ROLLBACK:
            state.rollback()

        elif self.action_type == ActionType.NOOP:
            pass

    def __repr__(self):
        return f"Action({self.action_type.name}, {self.parameter})"



