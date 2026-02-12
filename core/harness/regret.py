class Regret:
    @staticmethod
    def compute(agent_cost, reference_cost):
        return agent_cost - reference_cost
