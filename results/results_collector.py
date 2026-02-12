# results/results_collector.py
# SFR-BR v3 — Results Collector
# Sprint 7.2.1
#
# Purpose:
#   - Canonical collection of experiment results
#   - No computation, no aggregation, no interpretation
#   - Deterministic and replay-safe
#
# This file is FROZEN once Sprint 7.2 completes.

from typing import Dict, List


class ResultsCollector:
    """
    Collects per-run experiment results into a structured table.

    Each row corresponds to EXACTLY ONE experiment configuration:
        (agent × failure × run)

    This class MUST remain logic-free.
    """

    def __init__(self):
        self._rows: List[Dict] = []

    def record(self, row: Dict):
        """
        Record a single experiment result.

        Required keys (validated at runtime):
            agent_name
            failure_type
            dt_inject
            dti
            recovery_success
            recovery_cost
            hard_cap_hit
            semantic_drift_detected
            srv
            determinism_pass
        """

        required_fields = [
            "agent_name",
            "failure_type",
            "dt_inject",
            "dti",
            "recovery_success",
            "recovery_cost",
            "hard_cap_hit",
            "semantic_drift_detected",
            "srv",
            "determinism_pass",
        ]

        missing = [k for k in required_fields if k not in row]
        if missing:
            raise ValueError(
                f"ResultsCollector: missing required fields: {missing}"
            )

        # Defensive copy to prevent mutation
        self._rows.append(dict(row))

    def rows(self) -> List[Dict]:
        """
        Returns raw rows (read-only intent).
        """
        return list(self._rows)

    def to_dataframe(self):
        """
        Convert results to a Pandas DataFrame.
        Used ONLY in Sprint 7.2+ scripts.
        """
        try:
            import pandas as pd
        except ImportError:
            raise RuntimeError(
                "Pandas is required for DataFrame export"
            )

        return pd.DataFrame(self._rows)

    def to_csv(self, path: str):
        """
        Persist results as CSV.
        """
        df = self.to_dataframe()
        df.to_csv(path, index=False)

    def to_json(self, path: str):
        """
        Persist results as JSON.
        """
        import json

        with open(path, "w") as f:
            json.dump(self._rows, f, indent=2)
