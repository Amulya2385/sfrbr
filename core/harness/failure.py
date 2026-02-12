# harness/failure.py
# Sprint 8.4 — Deterministic Latent KV Poisoning

class SilentFailure:
    """
    Generic failure wrapper.
    """

    def __init__(self, apply_fn):
        self._apply_fn = apply_fn

    def apply(self, state, step):
        self._apply_fn(state, step)


class SilentFailureInjector:
    """
    Failure factory.
    All methods return SilentFailure objects.
    """

    # -------------------------------------------------------
    # Deterministic Latent KV Poisoning
    # -------------------------------------------------------
    @staticmethod
    def latent_kv_poisoning(
        start_step,
        token_start,
        token_end,
        detection_probability=0.3,
    ):
        """
        Injects latent KV corruption at a given step.
        Detection delay is deterministic:
            delay = ceil(1 / detection_probability)
        """

        def apply(state, step):

            if step == start_step and hasattr(state, "kv_cache"):
                kv = state.kv_cache

                kv.poison(
                    start_token=token_start,
                    end_token=token_end,
                    current_step=step,
                    detection_probability=detection_probability,
                )

        return SilentFailure(apply)

    # -------------------------------------------------------
    # Backward Compatibility
    # -------------------------------------------------------
    @staticmethod
    def multi_phase_failure(*args, **kwargs):
        return SilentFailureInjector.latent_kv_poisoning(
            start_step=1,
            token_start=0,
            token_end=16,
            detection_probability=0.3,
        )








