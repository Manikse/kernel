import os
import sys
import asyncio
import requests
import time
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel
from openai import AsyncOpenAI

# Твої драйвери та ядро
from drivers.terminal import TerminalDriver
from drivers.web_search import WebSearchDriver
from drivers.file_system import FileSystemDriver
from kernel.unms.memory import UNMSController
from kernel.runtime.loop import KernelRuntime

# БЕЗПЕЧНИЙ ФІКС КОДУВАННЯ
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        pass

class OpenRouterProvider(LLMProvider):
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
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Kernel Error: {str(e)}"

class OllamaProvider(LLMProvider):
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
                None, lambda: requests.post(self.base_url, json=payload, timeout=300)
            )
            response.raise_for_status()
            return response.json().get("response", "Error: Empty response.")
        except Exception as e:
            return f"Kernel Error: {str(e)}"

class ACLController:
    def __init__(self):
        self.providers = {}
        self.primary = None
        self.backup = None
        self.primary_status = "UNKNOWN"
        self._lock = asyncio.Lock()

    def register_provider(self, name: str, provider: LLMProvider, is_primary=False):
        self.providers[name] = provider
        if is_primary:
            self.primary = name
        elif not self.backup:
            self.backup = name

    async def health_check(self):
        if self.primary:
            test_response = await self.providers[self.primary].generate("ping", "Reply with pong")
            if "Kernel Error" in test_response:
                self.primary_status = "FAILED"
                return False
            self.primary_status = "ONLINE"
            return True
        return False

    async def execute(self, prompt: str, system_prompt: str = "") -> str:
        sys_prompt = system_prompt or "You are ExArchon, a Cognitive OS."

        async with self._lock:
            if self.primary and self.primary_status == "ONLINE":
                result = await self.providers[self.primary].generate(prompt, sys_prompt)
                if "Kernel Error" not in result:
                    return result
                
            if self.backup:
                return await self.providers[self.backup].generate(prompt, sys_prompt)

            return "CRITICAL ERROR: Усі когнітивні центри офлайн."

# --- ТИХИЙ ФОНОВИЙ ДЕМОН (Без виклику Kernel Tools) ---
async def daemon_worker(acl, console):
    console.print("[dim italic] Daemon worker initialized...[/dim italic]\n")
    os.makedirs("kernel_workspace", exist_ok=True)
    
    while True:
        await asyncio.sleep(120) 
        console.print("\n[dim cyan]🕰️ [Daemon] Executing silent background check...[/dim cyan]")
        try:
            # Демон просто просить короткий текст напряму в нейромережі, без інструментів і планувальників
            status_text = await acl.execute(
                prompt="Згенеруй ОДНЕ дуже коротке речення для технічного логу про те, що система працює стабільно. Тільки суть.",
                system_prompt="You are a silent background logging process."
            )
            
            # Пишемо у файл засобами Python (жодних повідомлень в консоль про FileSystem)
            with open("kernel_workspace/daemon_status.log", "a", encoding="utf-8") as f:
                f.write(f"[{time.ctime()}] {status_text.strip()}\n")
                
            console.print("[dim green]✅ [Daemon] Check complete. Log saved.[/dim green]")
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
                console.print("\n[bold red]Suspending all Kernel processes. Goodbye.[/]")
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
    await asyncio.sleep(0.5)
    
    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_API_KEY") 
    
    acl = ACLController()
    
    with console.status("[bold blue]Performing Cognitive Diagnostics (Ping)...", spinner="dots"):
        if API_KEY:
            acl.register_provider("OpenRouter Cloud", OpenRouterProvider(api_key=API_KEY), is_primary=True)
            acl.register_provider("Llama Edge", OllamaProvider(), is_primary=False)
            
            cloud_ok = await acl.health_check()
            if cloud_ok:
                status_acl = "[bold green]HYBRID (Cloud Active)[/]"
            else:
                status_acl = "[bold red]HYBRID DOWN (API Key Error) -> EDGE ONLY[/]"
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
                                                                 
    [white]EXARCHON COGNITIVE OS LAYER // ALPHA v0.9.3[/white]
    [/bold cyan]
    """
    
    status_table = (
        f"● [bold white]ACL Layer:[/] {status_acl}\n"
        f"● [bold white]UNMS Memory:[/] [bold green]READY[/]\n"
        f"● [bold white]Drivers active:[/] [bold cyan]Terminal, WebSearch, FileSystem[/]\n"
        f"● [bold white]Daemon Worker:[/] [bold green]ONLINE (Silent Mode)[/]"
    )
    
    console.print(logo)
    console.print(Panel(status_table, title="[bold white]System Status[/]", border_style="dim", expand=False))
    
    start_time = asyncio.get_event_loop().time()

    # ЗВЕРНИ УВАГУ: Передаємо acl замість kernel
    daemon_task = asyncio.create_task(daemon_worker(acl, console))
    repl_task = asyncio.create_task(interactive_repl(kernel, console, start_time))
    
    await asyncio.gather(daemon_task, repl_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass