# harness/state.py
# Sprint 8.2 — State aligned with Latent KV Poisoning

from copy import deepcopy
from core.harness.kv_cache import KVCacheState


class State:
    def __init__(self):
        self.memory = {}
        self.step = 0
        self.tool_calls = 0

        # KV Cache (Sprint 8 model)
        self.kv_cache = KVCacheState()

        # Optional future compatibility
        self.tool_cache = {}

    # --------------------------------------------------
    # Deep Clone for Future Probes
    # --------------------------------------------------
    def clone(self):
        new = State()

        new.memory = deepcopy(self.memory)
        new.step = self.step
        new.tool_calls = self.tool_calls

        # Proper KV clone
        new.kv_cache.tokens = self.kv_cache.tokens
        new.kv_cache.poisoned = self.kv_cache.poisoned
        new.kv_cache.detected = self.kv_cache.detected
        new.kv_cache.latent = self.kv_cache.latent   # ✅ FIXED

        new.tool_cache = deepcopy(self.tool_cache)

        return new

    # --------------------------------------------------
    # Optional rollback hook
    # --------------------------------------------------
    def rollback(self):
        self.step = max(0, self.step - 1)



