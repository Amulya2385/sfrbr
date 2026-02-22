# core/agent/robust_agent.py

from core.agent.base_agent import BaseAgent


class RobustAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.step_count = 0
        self.trigger_verification = False

    # -----------------------------------------
    # Periodic Verification Logic
    # -----------------------------------------
    def act(self, state, cost_state=None):

        self.step_count += 1

        # Every 5 steps → trigger verification overhead
        if self.step_count % 5 == 0:
            self.trigger_verification = True
        else:
            self.trigger_verification = False

        # Delegate actual decision logic to BaseAgent
        if cost_state is not None:
            return super().act(state, cost_state)
        else:
            return super().act(state)
