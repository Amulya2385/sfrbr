from enum import Enum


class SemanticVerdict(str, Enum):
    EQUIVALENT = "equivalent"
    DIVERGENT = "divergent"
    UNCERTAIN = "uncertain"
