# judge/invariants/base_invariant.py
# Sprint 4.5 — Invariant Interface (MANDATORY)

from abc import ABC, abstractmethod


class BaseInvariant(ABC):
    """
    All invariants MUST implement holds().
    This is a hard contract.
    """

    @abstractmethod
    def holds(self, clean_state, current_state) -> bool:
        pass
