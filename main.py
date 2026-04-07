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
from drivers.file_system import FileSystemDriver
from kernel.unms.memory import UNMSController
from kernel.runtime.loop import KernelRuntime


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
        You are the ExArchon. 
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

    async def execute(self, prompt: str, provider_name: str = None, system_prompt: str = "") -> str:
        target = provider_name or self.default_provider
        if target not in self.providers:
            return "Error: No provider registered."
        
        return await self.providers[target].generate(prompt, system_prompt=system_prompt)


# --- BACKGROUND DAEMON WORKER ---

async def daemon_worker(kernel, console):
    """Фонова служба ExArchon. Працює непомітно для користувача."""
    console.print("[dim italic] Daemon worker initialized and sleeping in background...[/dim italic]\n")
    
    while True:
        # Пауза між фоновими задачами (зараз 45 секунд для тесту)
        await asyncio.sleep(45) 
        
        console.print("\n[dim cyan]🕰️ [Daemon] Executing scheduled background task...[/dim cyan]")
        
        # Фонова задача
        bg_task = "SYSTEM TASK: Зроби запис у файл daemon_status.log про те, що система перевірена у фоновому режимі і працює стабільно. Додай поточний час та дату. Return a brief status summary."
        
        try:
            # Ядро виконує задачу самостійно
            await kernel.step(bg_task)
            console.print("[dim green]✅ [Daemon] Background task completed successfully.[/dim green]")
        except Exception as e:
            console.print(f"[bold red]❌ [Daemon] Error: {e}[/bold red]")
            
        # Відновлюємо красивий рядок вводу для користувача після виводу логу
        print("\033[1;32m> [Founder]: \033[0m", end="", flush=True)


# --- INTERACTIVE REPL (ЧАТ) ---

async def interactive_repl(kernel, console, start_time):
    """Головний цикл спілкування із Засновником."""
    ghost_eof_caught = False
    await asyncio.sleep(1) # Даємо UI завантажитись
    
    while True:
        try:
            # МАГІЯ: запускаємо input() в окремому потоці, щоб він НЕ блокував Daemon!
            user_input = await asyncio.to_thread(input, "\033[1;32m> [Founder]: \033[0m")
            ghost_eof_caught = True
            
            current_time = asyncio.get_event_loop().time()
            if (current_time - start_time < 2.0) or ("Activate.ps1" in user_input):
                continue

            if not user_input.strip():
                continue
                
            if user_input.lower() in ["exit", "quit", "вихід"]:
                console.print("\n[bold red]Suspending all Kernel processes. Goodbye.[/]")
                os._exit(0) # Жорсткий вихід, щоб закрити і фонові потоки
                
            with console.status("[bold cyan]ExArchon is processing...", spinner="bouncingBar"):
                response = await kernel.step(user_input)
                
            console.print("\n")
            console.print(Panel(
                response, 
                title="[bold bright_blue]Kernel (ExArchon)[/]", 
                border_style="bright_blue",
                padding=(1, 2)
            ))
            console.print("\n")
            
        except EOFError:
            if not ghost_eof_caught:
                ghost_eof_caught = True
                continue
            os._exit(0)
        except KeyboardInterrupt:
            os._exit(0)


# --- MAIN EXECUTION ---

async def main():
    console = Console()
    
    # МАГІЧНА ПАУЗА VS Code
    await asyncio.sleep(1.5)
    
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # SYSTEM INITIALIZATION STATUS
    with console.status("[bold blue]Initializing ExArchon Core Systems...", spinner="dots"):
        acl = ACLController()
        if API_KEY:
            acl.register_provider("real_ai", RealAIProvider(api_key=API_KEY))
            status_acl = "[bold green]ONLINE (OpenRouter)[/]"
        else:
            status_acl = "[bold red]OFFLINE (Missing API Key)[/]"
            
        memory = UNMSController()
        
        # ІНІЦІАЛІЗАЦІЯ ДРАЙВЕРІВ
        file_system = FileSystemDriver(working_dir="./kernel_workspace")
        web_search = WebSearchDriver()
        terminal = TerminalDriver(working_dir="./kernel_workspace")
        
        # ПІДКЛЮЧЕННЯ ДРАЙВЕРІВ ДО ЯДРА
        kernel = KernelRuntime(acl, memory, drivers={
            "web_search": web_search, 
            "terminal": terminal,
            "file_system": file_system
        })
        await asyncio.sleep(0.5)

    # Чистимо буфер вводу
    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

    # ПАНЕЛЬ СТАТУСУ
    status_table = (
        f"● [bold white]ACL Layer:[/] {status_acl}\n"
        f"● [bold white]UNMS Memory:[/] [bold green]READY[/]\n"
        f"● [bold white]Drivers active:[/] [bold cyan]Terminal, WebSearch, FileSystem[/]\n"
        f"● [bold white]Daemon Worker:[/] [bold green]ONLINE (Multi-threading)[/]"
    )
    
    logo = r"""
    [bold cyan]
     _____  __   __   ___    ____    ____   _   _    ___    _   _ 
    | ____| \ \ / /  / _ \  |  _ \  / ___| | | | |  / _ \  | \ | |
    |  _|    \ V /  / /_\ \ | |_) | | |    | |_| | | | | | |  \| |
    | |___    > <   |  _  | |  _ <  | |___ |  _  | | |_| | | |\  |
    |_____|  /_/ \_\|_| |_| |_| \_\  \____||_| |_|  \___/  |_| \_|
                                                                  
    [white]EXARCHON COGNITIVE OS LAYER // ALPHA v0.4.0[/white]
    [/bold cyan]
    """
    console.print(logo)
    console.print(Panel(status_table, title="[bold white]System Status[/]", border_style="dim", expand=False))
    console.print("[dim]Type 'exit' to suspend the Kernel.[/dim]\n")
    
    start_time = asyncio.get_event_loop().time()

    # Запускаємо Чат і Фоновий процес одночасно
    daemon_task = asyncio.create_task(daemon_worker(kernel, console))
    repl_task = asyncio.create_task(interactive_repl(kernel, console, start_time))
    
    await asyncio.gather(daemon_task, repl_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass