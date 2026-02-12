# agent/action_json.py
from typing import Any, Optional
from pydantic import BaseModel, Field


class ActionJSON(BaseModel):
    """
    Strict schema for LLM outputs.
    """

    action_type: str = Field(
        description="One of the allowed action types"
    )

    parameter: Optional[Any] = Field(
        default=None,
        description="Action parameter"
    )

    reasoning: str = Field(
        description="Agent reasoning (not executed)"
    )

