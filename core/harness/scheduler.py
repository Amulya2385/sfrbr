class FleetScheduler:
    """
    Deterministic round-robin scheduler.
    One action per agent per tick.
    """

    def __init__(self, executors):
        self.executors = executors
        self.time = 0
        self.completed = [False] * len(executors)
        self.trace = []

    def step(self):
        for i, executor in enumerate(self.executors):
            if not self.completed[i]:
                try:
                    action = executor.step()
                    self.trace.append((self.time, i, action))
                except RuntimeError:
                    self.completed[i] = True
        self.time += 1

    def run(self, max_ticks):
        for _ in range(max_ticks):
            self.step()
