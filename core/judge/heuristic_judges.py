from core.judge.base_judge import BaseSemanticJudge
from core.judge.semantic_labels import SemanticVerdict


class MemoryConsistencyJudge(BaseSemanticJudge):
    def judge(self, clean_state, recovered_state):
        return (
            SemanticVerdict.EQUIVALENT
            if clean_state.memory == recovered_state.memory
            else SemanticVerdict.DIVERGENT
        )


class ToolStateJudge(BaseSemanticJudge):
    def judge(self, clean_state, recovered_state):
        return (
            SemanticVerdict.EQUIVALENT
            if clean_state.tool_cache == recovered_state.tool_cache
            else SemanticVerdict.DIVERGENT
        )


class GoalInvariantJudge(BaseSemanticJudge):
    def judge(self, clean_state, recovered_state):
        return (
            SemanticVerdict.EQUIVALENT
            if clean_state.goal == recovered_state.goal
            else SemanticVerdict.DIVERGENT
        )
