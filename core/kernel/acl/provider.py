import os
from abc import ABC, abstractmethod
from openai import AsyncOpenAI

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        pass

class RealAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "google/gemini-2.0-flash-001"):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.model = model

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt or "You are the Kernel, a highly efficient AI OS layer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Kernel Error: {str(e)}"

class ACLController:
    def __init__(self):
        self.providers = {}
        self.default_provider = "real_ai"

    def register_provider(self, name: str, provider: LLMProvider):
        self.providers[name] = provider

    async def execute(self, prompt: str, provider_name: str = None, system_prompt: str = "") -> str:
        target = provider_name or self.default_provider
        if target not in self.providers:
            return "Error: No provider registered."
        # Передаємо system_prompt далі в генератор
        return await self.providers[target].generate(prompt, system_prompt=system_prompt)