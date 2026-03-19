import asyncio
import os
from abc import ABC, abstractmethod
from openai import AsyncOpenAI
from dotenv import load_dotenv
from drivers.terminal import TerminalDriver
# Імпортуємо тільки те, що реально лежить в інших файлах
from drivers.web_search import WebSearchDriver
from kernel.unms.memory import UNMSController
from kernel.runtime.loop import KernelRuntime
from drivers.file_system import FileDriver

# --- ACL SECTION ---

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
        # Наш маніфест ідентичності
        KERNEL_MANIFESTO = """
        You are the Kernel (MK-1). 
        You are created by Manikse.
        Manikse is a visionary founder building the future of AI.
        You are a Cognitive Operating System Layer.
        Your architecture consists of three core components: 
        - ACL (Agent Control Layer for Reasoning)
        - UNMS (Unified Neural Memory System)
        - A2A (Agent-to-Agent Protocol)
        Your purpose is to manage autonomous agents and interact with the physical world via Drivers.
        Respond in a professional, efficient, and visionary tone.
        
        IMPORTANT: You have access to Tools. Use them if needed.
        1. To search the internet, output EXACTLY: [SEARCH: your query]
        2. To run terminal commands/scripts (Powershell/CMD), output EXACTLY: [EXECUTE: your command]
        The system will intercept these, run them, and give you the output.
        """
        
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt or KERNEL_MANIFESTO},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Kernel Error: {str(e)}"

# ОСЬ КЛАС, ЯКОГО НЕ ВИСТАЧАЛО
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
    # 1. Завантажуємо змінні середовища з файлу .env
    load_dotenv()
    
    # 2. Безпечно дістаємо ключ
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # Захист від запуску без ключа
    if not API_KEY:
        print("\n[CRITICAL ERROR] OPENROUTER_API_KEY не знайдено!")
        print("Будь ласка, створи файл .env у корені проекту та додай рядок:")
        print("OPENROUTER_API_KEY=\"твій_секретний_ключ\"")
        return

    acl = ACLController()
    acl.register_provider("real_ai", RealAIProvider(api_key=API_KEY))
    
    memory = UNMSController()
    file_system = FileDriver(base_path="./kernel_workspace")
    web_search = WebSearchDriver() 
    terminal = TerminalDriver(working_dir="./kernel_workspace") # НОВИЙ ДРАЙВЕР

    # Передаємо драйвери в Ядро
    kernel = KernelRuntime(acl, memory, drivers={"web_search": web_search, "terminal": terminal})

    print("\n--- [Manikse Kernel (MK-1) IS ONLINE] ---")
    print("Type 'exit' to suspend the Kernel.\n")
    
    # Нескінченний цикл для реального спілкування
    while True:
        user_input = input("[Founder]: ")
        
        if user_input.lower() in ["exit", "quit", "вихід"]:
            print("[Kernel]: Suspending all processes. Goodbye.")
            break
            
        # Обробка запиту через ядро
        response = await kernel.step(user_input)
        print(f"\n[Kernel]: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())