from core.agent.base_agent import BaseAgent
from core.harness.executor import Executor
from tasks.task_definition import initial_state


def test_branch_determinism():
    agent = BaseAgent()

    exec1 = Executor(agent, initial_state())
    snap = exec1.run(steps=5, inject_at=2)

    restored_state = snap.restore()
    exec2 = Executor(agent, restored_state)
    exec2.run(steps=3)

    assert [a.action_type for a in exec1.trace[2:]] == \
           [a.action_type for a in exec2.trace]
