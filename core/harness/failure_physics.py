from core.harness.drift import GradualDrift


class FailureSchedule:
    def apply(self, state):
        raise NotImplementedError


class InstantFailure(FailureSchedule):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def apply(self, state):
        state[self.key] = self.value


class MultiPhaseFailure(FailureSchedule):
    """
    Phase 1: Instant corruption
    Phase 2: Gradual drift
    """

    def __init__(self, instant_failure, drift):
        self.instant_failure = instant_failure
        self.drift = drift
        self.phase = 0

    def apply(self, state):
        if self.phase == 0:
            self.instant_failure.apply(state)
            self.phase = 1
        else:
            self.drift.apply(state)
