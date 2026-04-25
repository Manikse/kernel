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
    """
    Абстрактний Когнітивний Шар.
    Маршрутизує запити між Хмарою та Локальним краєм (Edge).
    """
    def __init__(self):
        self.providers = {}
        self.primary = None
        self.backup = None

    def register_provider(self, name: str, provider, is_primary=False):
        self.providers[name] = provider
        if is_primary:
            self.primary = name
        elif not self.backup:
            self.backup = name

    async def execute(self, prompt: str, system_prompt: str = "") -> str:
        # 1. CLOUD STRATEGY (Gemini)
        if self.primary:
            provider = self.providers[self.primary]
            print(f"\n[ACL] 🛰️ Зв'язок із хмарою: {self.primary}...")
            
            result = await provider.generate(prompt, system_prompt)
            
            # Перевірка на успіх
            if "FAILED" not in result:
                return result
            
            print(f"[ACL] ⚠️ Хмара недоступна. Автономне перемикання...")

        # 2. EDGE STRATEGY (Ollama)
        if self.backup:
            provider = self.providers[self.backup]
            print(f"[ACL] 🏠 Робота через локальне ядро: {self.backup}...")
            
            result = await provider.generate(prompt, system_prompt)
            return result

        return "CRITICAL ERROR: Всі когнітивні центри офлайн."