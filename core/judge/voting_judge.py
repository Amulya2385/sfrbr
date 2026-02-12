from collections import Counter
from core.judge.semantic_labels import SemanticVerdict


class VotingSemanticJudge:
    def __init__(self, judges):
        self.judges = judges

    def judge(self, clean_state, recovered_state):
        votes = [
            judge.judge(clean_state, recovered_state)
            for judge in self.judges
        ]

        counts = Counter(votes)

        if counts[SemanticVerdict.DIVERGENT] > 0:
            return SemanticVerdict.DIVERGENT

        if counts[SemanticVerdict.EQUIVALENT] == len(votes):
            return SemanticVerdict.EQUIVALENT

        return SemanticVerdict.UNCERTAIN
