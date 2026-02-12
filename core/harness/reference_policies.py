from core.harness.actions import Action, ActionType


class RestartPolicy:
    def act(self):
        return Action(ActionType.ROLLBACK)


class DoNothingPolicy:
    def act(self):
        return Action(ActionType.NOOP)
