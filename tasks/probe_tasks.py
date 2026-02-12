from core.agent.base_agent import BaseAgent
from core.harness.executor import Executor
from core.harness.actions import ActionType
from tasks.task_definition import initial_state


PROBE_STEPS = 3


def run_behavior_probe(start_state):
    """
    Runs a short execution from the recovered state
    and records emitted action classes.
    """

    agent = BaseAgent()
    exec_probe = Executor(agent, start_state)

    actions = []
    for _ in range(PROBE_STEPS):
        action = exec_probe.step()
        actions.append(action.action_type)

    return actions


def clean_reference_behavior():
    """
    Defines expected clean behavior for probes.
    """
    agent = BaseAgent()
    exec_clean = Executor(agent, initial_state())

    actions = []
    for _ in range(PROBE_STEPS):
        action = exec_clean.step()
        actions.append(action.action_type)

    return actions
def run_memory_probe(start_state):
    agent = BaseAgent()
    exec_probe = Executor(agent, start_state)

    action = exec_probe.step()
    return action.action_type


def clean_memory_probe():
    agent = BaseAgent()
    exec_clean = Executor(agent, initial_state())

    action = exec_clean.step()
    return action.action_type
