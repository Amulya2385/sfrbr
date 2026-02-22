# core/harness/recovery_executor.py
# Sprint 8.4 — Deterministic Detection Lag + Elastic Budget
# + Robust Periodic Verification Overhead

from core.agent.actions import Action, ActionType
from core.judge.stub_judge import StubSemanticJudge
from core.harness.cost_state import CostState


class RecoveryExecutor:
    def __init__(
        self,
        agent,
        state,
        budget,
        cost_simulator,
        semantic_judge=None,
        clean_snapshot=None,
    ):
        self.agent = agent
        self.state = state
        self.budget = budget
        self.cost_simulator = cost_simulator

        self.semantic_judge = semantic_judge or StubSemanticJudge()
        self.clean_snapshot = clean_snapshot

        self.step_count = 0
        self.recovery_complete = False
        self.failed_due_to_hard_cap = False

        self.failure_schedule = None
        self.in_recovery = True

    # -----------------------------------------------------
    # ONE STEP
    # -----------------------------------------------------
    def step(self):

        # 1️⃣ Logic budget enforcement
        if self.budget.exceeded(self.step_count):
            raise RuntimeError("RECOVERY_BUDGET_EXCEEDED")

        # 2️⃣ Failure injection
        if self.failure_schedule:
            self.failure_schedule.apply(self.state, self.step_count)

        # 3️⃣ Deterministic Detection Lag
        if hasattr(self.state, "kv_cache"):
            self.state.kv_cache.maybe_detect(
                current_step=self.step_count
            )

        # 4️⃣ Elastic Cost Signal
        cost_state = CostState(
            total_cost=self.cost_simulator.total_cost,
            hard_cap=self.cost_simulator.hcv.hard_cost_cap,
            last_action_cost=self.cost_simulator.last_action_cost,
        )

        # 5️⃣ Agent action
        try:
            action = self.agent.act(self.state, cost_state)
        except TypeError:
            action = self.agent.act(self.state)

        if not isinstance(action, Action):
            raise RuntimeError("Agent must return Action instance")

        # 6️⃣ Charge action cost
        self.cost_simulator.charge(action)

        if self.cost_simulator.exceeded_hard_cap():
            self.failed_due_to_hard_cap = True
            raise RuntimeError("RECOVERY_FAILED_HARD_CAP")

        # 🔥 7️⃣ Periodic Verification Overhead (Robust Only)
        if hasattr(self.agent, "trigger_verification"):
            if self.agent.trigger_verification:
                if hasattr(self.state, "kv_cache"):

                    self.cost_simulator.charge_kv_recompute(
                        self.state.kv_cache
                    )

                    if self.cost_simulator.exceeded_hard_cap():
                        self.failed_due_to_hard_cap = True
                        raise RuntimeError(
                            "RECOVERY_FAILED_VERIFICATION_OVERHEAD"
                        )

        # 8️⃣ Apply action
        action.apply(self.state)

        # 9️⃣ KV logic
        if hasattr(self.state, "kv_cache"):

            # Context growth
            if action.action_type == ActionType.PLAN_EXPAND:
                self.state.kv_cache.expand(32)

            # Recompute if detected poison
            if self.state.kv_cache.poisoned and self.state.kv_cache.detected:

                self.cost_simulator.charge_kv_recompute(
                    self.state.kv_cache
                )

                self.state.kv_cache.recompute()

                if self.cost_simulator.exceeded_hard_cap():
                    self.failed_due_to_hard_cap = True
                    raise RuntimeError(
                        "RECOVERY_FAILED_KV_CACHE_OVERFLOW"
                    )

        # 🔟 Semantic guardrail
        if self.clean_snapshot and self.semantic_judge:
            verdict = self.semantic_judge.compare(
                clean_state=self.clean_snapshot._state,
                current_state=self.state,
            )
            if verdict == "DIVERGENT":
                raise RuntimeError("LOGICAL_DRIFT_DETECTED")

        self.step_count += 1
        return action














