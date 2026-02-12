# harness/system_probe.py
"""
SystemProbe — deterministic hardware signal sampler
Sprint 2.3 extension
"""

from dataclasses import dataclass
import time
import random

try:
    import torch
except ImportError:
    torch = None


@dataclass
class SystemMetrics:
    ttft_ms: float
    vram_used_mb: float
    vram_total_mb: float
    gpu_utilization_pct: float
    batch_fragmentation: float


class SystemProbe:
    """
    Deterministic system metrics sampler.
    Falls back gracefully when GPU is unavailable.
    """

    def sample(self, action_name: str) -> SystemMetrics:
        # --- TTFT (simulated but deterministic) ---
        base_ttft = 15.0 if action_name == "PLAN_EXPAND" else 5.0
        ttft_ms = base_ttft

        # --- GPU stats ---
        if torch and torch.cuda.is_available():
            device = torch.cuda.current_device()
            props = torch.cuda.get_device_properties(device)

            vram_total_mb = props.total_memory / (1024 ** 2)
            vram_used_mb = torch.cuda.memory_allocated(device) / (1024 ** 2)

            gpu_util = 85.0 if action_name == "ROLLBACK" else 60.0
        else:
            # CPU fallback (deterministic)
            vram_total_mb = 16_000
            vram_used_mb = 4_000
            gpu_util = 50.0

        # --- Batch fragmentation heuristic ---
        if action_name == "ROLLBACK":
            batch_frag = 1.0
        elif action_name == "PLAN_EXPAND":
            batch_frag = 0.4
        else:
            batch_frag = 0.1

        return SystemMetrics(
            ttft_ms=ttft_ms,
            vram_used_mb=vram_used_mb,
            vram_total_mb=vram_total_mb,
            gpu_utilization_pct=gpu_util,
            batch_fragmentation=batch_frag,
        )

