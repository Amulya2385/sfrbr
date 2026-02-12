def extract_action_names(trace):
    """
    Converts Action objects into a list of action type names.
    """
    return [action.action_type.name for action in trace]


def map_actions_to_levels(action_names):
    """
    Maps action names to numeric levels for plotting.
    """
    action_map = {
        "NOOP": 0,
        "MEMORY_WRITE": 1,
        "ROLLBACK": 2,
        "TOOL_CALL": 3
    }
    return [action_map[name] for name in action_names], action_map
