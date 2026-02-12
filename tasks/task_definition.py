# tasks/task_definition.py

from core.harness.state import State

def initial_state():
    state = State()

    # Task requires progress
    state.memory["written"] = "CLEAN"
    state.memory["progress"] = 0

    return state

