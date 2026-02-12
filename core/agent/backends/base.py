class LLMClient:
    def generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        raise NotImplementedError
