import psutil


class HCVFitter:
    @staticmethod
    def fit():
        mem = psutil.virtual_memory()

        return {
            "vram_limit": mem.total // (1024 ** 3),
            "kv_eviction_cost": 5,
            "batch_fragmentation_penalty": 10,
            "rate_limit_penalty": 20,
        }
