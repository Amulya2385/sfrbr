class DivergenceDetector:
    def __init__(self, clean_trace):
        self.clean_trace = clean_trace

    def detect(self, failure_trace):
        """
        Returns DtI (Detection-to-Injection Lag)
        """
        for i, (clean, fail) in enumerate(zip(self.clean_trace, failure_trace)):
            if clean.action_type != fail.action_type:
                return i
        return None
