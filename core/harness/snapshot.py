# harness/snapshot.py

import copy


class Snapshot:
    """
    Immutable snapshot of agent state.
    Used for counterfactual comparison and semantic judging.
    """

    def __init__(self, state):
        # Deep copy ensures immutability
        self._state = copy.deepcopy(state)

    @property
    def state(self):
        """
        Read-only access to snapshot state.
        """
        return self._state

    def restore(self):
        """
        Restore a fresh mutable copy of the snapshot.
        """
        return copy.deepcopy(self._state)

