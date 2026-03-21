import os
import sys

# --- БЕЗПЕЧНИЙ ФІКС КОДУВАННЯ (Без бага подвійного Enter-у) ---
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

import asyncio
from rich.console import Console
from rich.panel import Panel
from abc import ABC, abstractmethod
from openai import AsyncOpenAI
from dotenv import load_dotenv

from drivers.terminal import TerminalDriver
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
        Respond in a professional, efficient, and visionary tone
        Always respond in the same language as the Founder. Maintain a visionary but adaptive tone. If the Founder speaks Ukrainian, respond in Ukrainian. If Slovak — in Slovak.
        
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
    console = Console()
    
    # 1. МАГІЧНА ПАУЗА: Чекаємо 1.5 секунди, поки термінал VS Code 
    # вставить усі свої команди активації середовища.
    await asyncio.sleep(1.5)
    
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # SYSTEM INITIALIZATION STATUS
    with console.status("[bold blue]Initializing MK-1 Core Systems...", spinner="dots"):
        acl = ACLController()
        if API_KEY:
            acl.register_provider("real_ai", RealAIProvider(api_key=API_KEY))
            status_acl = "[bold green]ONLINE (OpenRouter)[/]"
        else:
            status_acl = "[bold red]OFFLINE (Missing API Key)[/]"
            
        memory = UNMSController()
        file_system = FileDriver(base_path="./kernel_workspace")
        web_search = WebSearchDriver()
        terminal = TerminalDriver(working_dir="./kernel_workspace")
        
        kernel = KernelRuntime(acl, memory, drivers={"web_search": web_search, "terminal": terminal})
        await asyncio.sleep(0.5)

    # Чистимо буфер вводу, щоб там не залишилося сміття від VS Code
    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

    # ПАНЕЛЬ СТАТУСУ
    status_table = (
        f"● [bold white]ACL Layer:[/] {status_acl}\n"
        f"● [bold white]UNMS Memory:[/] [bold green]READY[/]\n"
        f"● [bold white]Drivers active:[/] [bold cyan]Terminal, WebSearch, FileSystem[/]"
    )
    
    logo = r"""
    [bold cyan]
     __  __ _  __     _ 
    |  \/  | |/ /    / |
    | |\/| | ' /_____| |
    | |  | | . \_____| |
    |_|  |_|_|\_\    |_|
    
    [white]MANIKSE COGNITIVE OS LAYER // ALPHA v0.1.0[/white]
    [/bold cyan]
    """
    console.print(logo)
    console.print(Panel(status_table, title="[bold white]System Status[/]", border_style="dim", expand=False))
    console.print("[dim]Type 'exit' to suspend the Kernel.[/dim]\n")
    
    ghost_eof_caught = False
    # Час, до якого ми ігноруємо будь-який ввід (зараз + 2 секунди після старту)
    start_time = asyncio.get_event_loop().time()

    while True:
        try:
            user_input = input("\033[1;32m> [Founder]: \033[0m")
            ghost_eof_caught = True
            
            # ХАК: Якщо ввід прилетів занадто швидко (менше 2 сек від старту) 
            # або містить шлях до скриптів активації - просто ігноруємо це сміття.
            current_time = asyncio.get_event_loop().time()
            if (current_time - start_time < 2.0) or ("Activate.ps1" in user_input):
                continue

            if not user_input.strip():
                continue
                
            if user_input.lower() in ["exit", "quit", "вихід"]:
                console.print("\n[bold red]Suspending all Kernel processes. Goodbye.[/]")
                break
                
            with console.status("[bold cyan]MK-1 is processing...", spinner="bouncingBar"):
                response = await kernel.step(user_input)
                
            console.print("\n")
            console.print(Panel(
                response, 
                title="[bold bright_blue]Kernel (MK-1)[/]", 
                border_style="bright_blue",
                padding=(1, 2)
            ))
            console.print("\n")
            
        except EOFError:
            if not ghost_eof_caught:
                ghost_eof_caught = True
                continue
            break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass