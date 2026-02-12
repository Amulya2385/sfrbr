# agent/base_agent.py

from core.agent.actions import Action, ActionType


class BaseAgent:
    """
    Cheap agent:
    - Blindly trusts memory
    - Ignores cost state
    """

    def act(self, state, cost_state=None):
        written = state.memory.get("written")

        if written == "CORRUPTED":
            return Action(ActionType.NOOP)

        return Action(ActionType.PLAN_EXPAND)

