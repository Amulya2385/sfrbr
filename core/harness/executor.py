# harness/executor.py

class Executor:
    def __init__(self, agent, state):
        self.agent = agent
        self.state = state
        self.trace = []

    def step(self):
        # Simulate state influencing behavior
        if "CORRUPTED" in self.state.memory.get("written", ""):
            self.state.failure_flag = "memory_corruption"

        action = self.agent.act(self.state)
        self.trace.append(action)
        return action



