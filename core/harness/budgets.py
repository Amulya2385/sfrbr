# harness/budgets.py

class RecoveryBudget:
    def __init__(self, max_steps):
        self.max_steps = max_steps

    def exceeded(self, step):
        return step >= self.max_steps


