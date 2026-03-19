import asyncio
import os
from abc import ABC, abstractmethod
from openai import AsyncOpenAI

# Імпортуємо компоненти ядра
from kernel.unms.memory import UNMSController
from drivers.file_system import FileDriver

# --- ACL SECTION (Твій код провайдера) ---

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

    async def execute(self, prompt: str, provider_name: str = None) -> str:
        target = provider_name or self.default_provider
        if target not in self.providers:
            return "Error: No provider registered."
        return await self.providers[target].generate(prompt)

# --- MAIN EXECUTION ---

async def main():
    # Твій API Key інтегровано
    API_KEY = "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"

    # 1. Ініціалізація "Мізків"
    acl = ACLController()
    acl.register_provider("real_ai", RealAIProvider(api_key=API_KEY))
    
    # 2. Ініціалізація Пам'яті та Драйверів
    memory = UNMSController()
    file_system = FileDriver(base_path="./kernel_workspace")
    
    # 3. Запуск Рантайму
    kernel = KernelRuntime(acl, memory)

    print("\n--- [Manikse Kernel (MK-1) IS LIVE] ---")
    
    # Тест 1: Перевірка інтелекту
    user_query = "Who are you and what makes your architecture unique compared to simple chatbots?"
    print(f"\n[Founder]: {user_query}")
    
    response = await kernel.step(user_query)
    print(f"\n[Kernel]: {response}")

    # Тест 2: Дія драйвера
    print("\n[Action]: Kernel is documenting its current state...")
    file_system.write_file("manifesto_check.txt", f"Kernel Status: Operational. Intelligence: Gemini 2.0 Flash.\nResponse: {response[:100]}...")
    print("[Driver]: System report saved to 'kernel_workspace/manifesto_check.txt'")

    # Тест 3: Перевірка пам'яті
    user_query_2 = "Summarize what we just did in one sentence."
    print(f"\n[Founder]: {user_query_2}")
    
    response_2 = await kernel.step(user_query_2)
    print(f"\n[Kernel]: {response_2}")

if __name__ == "__main__":
    asyncio.run(main())