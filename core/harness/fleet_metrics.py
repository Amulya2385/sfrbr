class FleetMetrics:
    def __init__(self, clean_throughput, failure_throughput):
        self.clean_throughput = clean_throughput
        self.failure_throughput = failure_throughput

    def fleet_damage_index(self):
        """
        FDI = relative throughput degradation
        """
        if self.clean_throughput == 0:
            return 0.0
        return (self.clean_throughput - self.failure_throughput) / self.clean_throughput
