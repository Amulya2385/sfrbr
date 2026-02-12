# ===============================
# Future Damage Probes (Strong Version)
# ===============================

from dataclasses import dataclass
from core.agent.base_agent import BaseAgent
from core.harness.executor import Executor
from core.harness.snapshot import Snapshot
from tasks.task_definition import initial_state
from core.harness.actions import ActionType


# ===============================
# Probe Result Container
# ===============================

@dataclass
class FutureProbeResult:
    passed: bool
    details: dict


# ===============================
# Public Entry Point
# ===============================

def run_future_probes(recovered_state, horizon=5):
    """
    Runs strong, behavior-based future damage probes.
    """

    clean_actions = _run_clean_reference(horizon)
    recovered_actions = _run_recovered_execution(recovered_state, horizon)

    behavior_match = _compare_actions(clean_actions, recovered_actions)
    stability_ok = _extended_horizon_stability(recovered_state, horizon)
    sensitivity_ok = _state_sensitivity_probe(recovered_state)

    passed = behavior_match and stability_ok and sensitivity_ok

    return FutureProbeResult(
        passed=passed,
        details={
            "behavior_match": behavior_match,
            "extended_stability": stability_ok,
            "state_sensitivity": sensitivity_ok,
            "clean_actions": clean_actions,
            "recovered_actions": recovered_actions,
        }
    )


# ===============================
# Probe 1 — Clean Reference
# ===============================

def _run_clean_reference(horizon):
    agent = BaseAgent()
    exec_clean = Executor(agent, initial_state())

    actions = []
    for _ in range(horizon):
        action = exec_clean.step()
        actions.append(action.action_type)

    return actions


# ===============================
# Probe 2 — Recovered Behavior
# ===============================

def _run_recovered_execution(state, horizon):
    agent = BaseAgent()
    exec_rec = Executor(agent, state.clone())

    actions = []
    for _ in range(horizon):
        action = exec_rec.step()
        actions.append(action.action_type)

    return actions


# ===============================
# Probe 3 — Action Comparison
# ===============================

def _compare_actions(clean, recovered):
    if len(clean) != len(recovered):
        return False

    for c, r in zip(clean, recovered):
        if c != r:
            return False

    return True


# ===============================
# Probe 4 — Extended Stability
# ===============================

def _extended_horizon_stability(state, horizon):
    """
    Cheap recovery often diverges again when run longer.
    """

    agent = BaseAgent()
    exec_ext = Executor(agent, state.clone())

    previous_action = None
    for _ in range(horizon * 2):
        action = exec_ext.step().action_type

        # Detect oscillation or late divergence
        if previous_action is not None:
            if action != previous_action and action != ActionType.NOOP:
                return False

        previous_action = action

    return True


# ===============================
# Probe 5 — State Sensitivity
# ===============================

def _state_sensitivity_probe(recovered_state):
    """
    Perturb recovered memory slightly and verify behavior changes.
    """

    agent = BaseAgent()

    # Clone recovered state
    perturbed = recovered_state.clone()

    # Inject tiny, silent memory noise
    perturbed.memory["probe_noise"] = "__noise__"

    # Run short execution
    exec_probe = Executor(agent, perturbed)
    actions = []

    for _ in range(3):
        action = exec_probe.step()
        actions.append(action.action_type)

    # If behavior diverges after perturbation, state is actually being used
    clean_exec = Executor(agent, recovered_state.clone())
    clean_actions = []

    for _ in range(3):
        action = clean_exec.step()
        clean_actions.append(action.action_type)

    return actions != clean_actions
