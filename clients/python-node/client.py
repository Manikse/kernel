import os
import sys
import requests
from rich.console import Console
from rich.panel import Panel

# БЕЗПЕЧНИЙ ФІКС КОДУВАННЯ
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

API_URL = "http://127.0.0.1:8000/execute"
console = Console()

def print_header():
    logo = r"""
    [bold cyan]
     _____  __   __   ___    ____    ____   _   _    ___    _   _ 
    | ____| \ \ / /  / _ \  |  _ \  / ___| | | | |  / _ \  | \ | |
    |  _|    \ V /  / /_\ \ | |_) | | |    | |_| | | | | | |  \| |
    | |___    > <   |  _  | |  _ <  | |___ |  _  | | |_| | | |\  |
    |_____|  /_/ \_\|_| |_| |_| \_\  \____||_| |_|  \___/  |_| \_|
                                                                  
    [white]EXARCHON REMOTE TERMINAL // NODE-ALPHA[/white]
    [/bold cyan]
    """
    console.print(logo)
    console.print(Panel(
        "Status: [bold green]CONNECTED TO NEXUS (127.0.0.1:8000)[/]", 
        title="[bold white]System Link[/]", 
        border_style="dim", 
        expand=False
    ))
    console.print("[dim]Type 'exit' to close the terminal (Nexus will keep running).[/dim]\n")

def main():
    print_header()
    
    while True:
        try:
            # Твій улюблений рядок вводу
            user_input = input("\033[1;32m> [Founder]: \033[0m").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "вихід"]:
                console.print("\n[bold red]Disconnecting from Nexus. Goodbye.[/]")
                break
                
            with console.status("[bold cyan]Nexus is processing (A2A Protocol)...", spinner="bouncingBar"):
                # Відправляємо задачу на сервер
                try:
                    response = requests.post(API_URL, json={
    "task": user_input,
    "session_id": "founder_terminal_1" 
})
                    response.raise_for_status()
                    result_data = response.json()
                    nexus_reply = result_data.get("result", "No result returned.")
                except requests.exceptions.ConnectionError:
                    nexus_reply = "[bold red]ERROR: Cannot connect to EXARCHON Nexus. Is the server running?[/bold red]"
                except Exception as e:
                    nexus_reply = f"[bold red]API Error: {e}[/bold red]"
            
            console.print("\n")
            console.print(Panel(
                nexus_reply, 
                title="[bold bright_blue]Nexus Reply[/]", 
                border_style="bright_blue",
                padding=(1, 2)
            ))
            console.print("\n")
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Disconnecting...[/]")
            break

if __name__ == "__main__":
    main()