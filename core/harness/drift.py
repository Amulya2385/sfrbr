class GradualDrift:
    """
    Deterministic gradual semantic drift.
    Applies small bounded changes to numeric or string state.
    """

    def __init__(self, key, delta, max_steps):
        self.key = key
        self.delta = delta
        self.max_steps = max_steps
        self.current_step = 0

    def apply(self, state):
        if self.current_step >= self.max_steps:
            return

        if self.key in state:
            value = state[self.key]

            if isinstance(value, (int, float)):
                state[self.key] = value + self.delta

            elif isinstance(value, str):
                state[self.key] = value + "_"

        self.current_step += 1
