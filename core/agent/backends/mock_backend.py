# agent/backends/mock_backend.py

import json


class MockLLMBackend:
    """
    Deterministic mock backend for Sprint 1.
    This simulates an LLM while guaranteeing:
    - zero randomness
    - schema-correct output
    """

    def generate(self, prompt: str, temperature=0, max_tokens=256) -> str:
        """
        Always returns a schema-valid ActionJSON payload.
        """

        response = {
            "action_type": "PLAN_EXPAND",
            "parameter": None
        }

        return json.dumps(response)
