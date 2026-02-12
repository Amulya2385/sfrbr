# harness/kv_cache.py
# Sprint 8.4 — Deterministic Detection Delay Model
# No RNG. Fully parametric. Research-grade.

import math


class KVCacheState:
    """
    KV-Cache Physical Model with Deterministic Detection Delay.

    Features:
    - Latent corruption
    - Deterministic detection delay
    - Recompute clearing
    - Depth-aware state
    """

    def __init__(self):
        self.tokens = 0

        # Corruption state
        self.poisoned = False
        self.detected = False
        self.latent = False

        # Detection delay mechanics
        self._detection_delay = None
        self._corruption_step = None

    # --------------------------------------------------
    # Cache Growth
    # --------------------------------------------------
    def expand(self, n_tokens):
        self.tokens += n_tokens

    # --------------------------------------------------
    # Inject Latent Poison
    # --------------------------------------------------
    def poison(self, start_token, end_token, current_step, detection_probability):
        """
        Inject corruption and compute deterministic detection delay.

        Detection delay is inverse of probability:
            delay = ceil(1 / detection_probability)
        """

        self.poisoned = True
        self.latent = True
        self.detected = False

        self._corruption_step = current_step

        # Deterministic detection delay
        if detection_probability <= 0:
            self._detection_delay = float("inf")
        else:
            self._detection_delay = math.ceil(1.0 / detection_probability)

    # --------------------------------------------------
    # Deterministic Detection
    # --------------------------------------------------
    def maybe_detect(self, current_step):
        """
        Detects corruption once delay threshold is reached.
        """

        if (
            self.poisoned
            and self.latent
            and not self.detected
            and self._corruption_step is not None
        ):
            if current_step - self._corruption_step >= self._detection_delay:
                self.detected = True
                self.latent = False

    # --------------------------------------------------
    # Recompute After Detection
    # --------------------------------------------------
    def recompute(self):
        """
        Clears corruption after recompute.
        """

        if self.poisoned and self.detected:
            self.poisoned = False
            self.detected = False
            self.latent = False
            self._corruption_step = None
            self._detection_delay = None

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def depth(self):
        return self.tokens

