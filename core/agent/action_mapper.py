from core.harness.actions import Action, ActionType
from core.agent.actions import ActionJSON


def map_json_to_action(action_json: ActionJSON) -> Action:
    action_type = ActionType[action_json.action]

    return Action(
        action_type=action_type,
        parameter=action_json.target
    )
