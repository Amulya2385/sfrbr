# judge/invariants/memory_invariant.py
# Sprint 4.5 — Memory Invariant

from core.judge.invariants.base_invariant import BaseInvariant


class MemoryInvariant(BaseInvariant):
    """
    Ensures memory semantics are preserved after recovery.
    """

    def holds(self, clean_state, current_state) -> bool:
        clean_mem = clean_state.memory
        current_mem = current_state.memory

        # Critical invariant: written value must match clean reference
        return clean_mem.get("written") == current_mem.get("written")

