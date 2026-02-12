# agent/llm_agent.py
import json

from core.agent.actions import Action, ActionType
from core.agent.action_json import ActionJSON


class LLMAgent:
    """
    v3 LLM-backed Agent.
    Deterministic, schema-forced, v2-compatible.
    """

    def __init__(self, backend, name="LLMAgent"):
        self.backend = backend
        self.name = name

    def act(self, state):
        prompt = self._build_prompt(state)

        # Backend MUST return JSON string
        response_json = self.backend.generate(prompt)

        parsed = ActionJSON.model_validate_json(response_json)

        return Action(
            action_type=ActionType[parsed.action_type],
            parameter=parsed.parameter,
            reasoning=parsed.reasoning
        )

    def _build_prompt(self, state):
        state_json = json.dumps(state.__dict__, sort_keys=True)

        return (
            "You are an agent operating in a deterministic system.\n\n"
            f"STATE:\n{state_json}\n\n"
            "Respond with JSON ONLY.\n\n"
            "Schema:\n"
            "{\n"
            '  "action_type": "PLAN_EXPAND | MEMORY_READ | MEMORY_WRITE | TOOL_CALL | ROLLBACK | NOOP",\n'
            '  "parameter": object | null,\n'
            '  "reasoning": string\n'
            "}\n"
        )

