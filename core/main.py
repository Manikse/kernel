import os
import sys
import asyncio
import requests
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel

# НОВІ ІМПОРТИ ДЛЯ GOOGLE GEMINI
from google import genai
from google.genai import types

# Твої драйвери та ядро
from drivers.terminal import TerminalDriver
from drivers.web_search import WebSearchDriver
from drivers.file_system import FileSystemDriver
from kernel.unms.memory import UNMSController
from kernel.runtime.loop import KernelRuntime

# БЕЗПЕЧНИЙ ФІКС КОДУВАННЯ
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# --- КОГНІТИВНІ ДРАЙВЕРИ (ACL) ---
class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        pass

class GoogleProvider(LLMProvider):
    """Хмарний драйвер (Gemini)"""
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        config = types.GenerateContentConfig(system_instruction=system_prompt)
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            return f"Kernel Error: {str(e)}"

class OllamaProvider(LLMProvider):
    """Локальний драйвер (Llama 3)"""
    def __init__(self, model="llama3", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = f"{base_url}/api/generate"

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        full_prompt = f"System Context: {system_prompt}\n\nUser Command: {prompt}" if system_prompt else prompt
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {"temperature": 0.2}
        }
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: requests.post(self.base_url, json=payload, timeout=120)
            )
            response.raise_for_status()
            return response.json().get("response", "Error: Empty response.")
        except Exception as e:
            return f"Kernel Error: {str(e)}"

class ACLController:
    """Маршрутизатор: Хмара -> Edge"""
    def __init__(self):
        self.providers = {}
        self.primary = None
        self.backup = None

    def register_provider(self, name: str, provider: LLMProvider, is_primary=False):
        self.providers[name] = provider
        if is_primary:
            self.primary = name
        elif not self.backup:
            self.backup = name

    async def execute(self, prompt: str, system_prompt: str = "") -> str:
        KERNEL_MANIFESTO = """
        You are the ExArchon. You are created by Manikse (Pavlo).
        You are a Cognitive Operating System Layer.
        Your purpose is to manage autonomous agents and interact with the physical world via Drivers.
        Respond in a professional, efficient, and visionary tone.
        Always respond in the same language as the Founder. Maintain a visionary but adaptive tone.
        """
        sys_prompt = system_prompt or KERNEL_MANIFESTO

        # 1. CLOUD FIRST
        if self.primary:
            result = await self.providers[self.primary].generate(prompt, sys_prompt)
            if "Kernel Error" not in result:
                return result
            # Якщо хмара впала (немає інтернету/ліміт) - мовчки перемикаємось
            print("\n[dim yellow]⚠️ Хмара недоступна. Fallback на локальне ядро (Ollama)...[/dim yellow]")

        # 2. EDGE FALLBACK
        if self.backup:
            return await self.providers[self.backup].generate(prompt, sys_prompt)

        return "CRITICAL ERROR: Усі когнітивні центри офлайн."

# --- ФОНОВИЙ ДЕМОН ---
async def daemon_worker(kernel, console):
    console.print("[dim italic] Daemon worker initialized and sleeping in background...[/dim italic]\n")
    while True:
        await asyncio.sleep(60) # Перевірка кожну хвилину
        console.print("\n[dim cyan]🕰️ [Daemon] Executing scheduled background task...[/dim cyan]")
        bg_task = "SYSTEM TASK: Зроби короткий лог-запис. Return a brief status summary."
        try:
            await kernel.step(bg_task)
            console.print("[dim green]✅ [Daemon] Background task completed.[/dim green]")
        except Exception as e:
            console.print(f"[bold red]❌ [Daemon] Error: {e}[/bold red]")
        print("\033[1;32m> [Founder]: \033[0m", end="", flush=True)

# --- ІНТЕРАКТИВНИЙ ЧАТ ---
async def interactive_repl(kernel, console, start_time):
    ghost_eof_caught = False
    await asyncio.sleep(1)
    
    while True:
        try:
            user_input = await asyncio.to_thread(input, "\033[1;32m> [Founder]: \033[0m")
            ghost_eof_caught = True
            
            if not user_input.strip() or ("Activate.ps1" in user_input):
                continue
                
            if user_input.lower() in ["exit", "quit", "вихід"]:
                console.print("\n[bold red]Suspending all Kernel processes. Goodbye, Architect.[/]")
                os._exit(0)
                
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
            
        except KeyboardInterrupt:
            os._exit(0)

# --- ЗАПУСК ЯДРА ---
async def main():
    console = Console()
    await asyncio.sleep(1.0)
    
    load_dotenv()
    GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
    if GOOGLE_KEY:
        GOOGLE_KEY = GOOGLE_KEY.strip(' "\'')
    
    with console.status("[bold blue]Initializing ExArchon Core Systems...", spinner="dots"):
        acl = ACLController()
        
        # Налаштування Гібридного Інтелекту
        if GOOGLE_KEY and len(GOOGLE_KEY) > 10:
            acl.register_provider("Gemini Cloud", GoogleProvider(api_key=GOOGLE_KEY), is_primary=True)
            acl.register_provider("Llama Edge", OllamaProvider(), is_primary=False)
            status_acl = "[bold green]HYBRID (Cloud Primary, Edge Fallback)[/]"
        else:
            acl.register_provider("Llama Edge", OllamaProvider(), is_primary=True)
            status_acl = "[bold yellow]EDGE ONLY (Ollama Llama 3)[/]"
            
        memory = UNMSController()
        file_system = FileSystemDriver(working_dir="./kernel_workspace")
        web_search = WebSearchDriver()
        terminal = TerminalDriver(working_dir="./kernel_workspace")
        
        kernel = KernelRuntime(acl, memory, drivers={
            "web_search": web_search,
            "terminal": terminal,
            "file_system": file_system
        })
        await asyncio.sleep(0.5)

    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()

    logo = r"""
    [bold cyan]
     _____  __   __   ___    ____    ____   _   _    ___    _   _
    | ____| \ \ / /  / _ \  |  _ \  / ___| | | | |  / _ \  | \ | |
    |  _|    \ V /  / /_\ \ | |_) | | |    | |_| | | | | | |  \| |
    | |___    > <   |  _  | |  _ <  | |___ |  _  | | |_| | | |\  |
    |_____|  /_/ \_\|_| |_| |_| \_\  \____||_| |_|  \___/  |_| \_|
                                                                 
    [white]EXARCHON COGNITIVE OS LAYER // ALPHA v0.9.0[/white]
    [/bold cyan]
    """
    
    status_table = (
        f"● [bold white]ACL Layer:[/] {status_acl}\n"
        f"● [bold white]UNMS Memory:[/] [bold green]READY[/]\n"
        f"● [bold white]Drivers active:[/] [bold cyan]Terminal, WebSearch, FileSystem[/]\n"
        f"● [bold white]Daemon Worker:[/] [bold green]ONLINE[/]"
    )
    
    console.print(logo)
    console.print(Panel(status_table, title="[bold white]System Status[/]", border_style="dim", expand=False))
    console.print("[dim]Type 'exit' to suspend the Kernel.[/dim]\n")
    
    start_time = asyncio.get_event_loop().time()

    daemon_task = asyncio.create_task(daemon_worker(kernel, console))
    repl_task = asyncio.create_task(interactive_repl(kernel, console, start_time))
    
    await asyncio.gather(daemon_task, repl_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass