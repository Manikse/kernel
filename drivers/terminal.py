import subprocess
import os

class TerminalDriver:
    """
    Драйвер терміналу. Дає Ядру 'руки' для виконання команд та скриптів.
    """
    def __init__(self, working_dir: str = "./kernel_workspace"):
        self.name = "Terminal"
        self.working_dir = working_dir
        # Переконуємось, що робоча папка існує
        if not os.path.exists(self.working_dir):
            os.makedirs(self.working_dir)

    def execute(self, command: str) -> str:
        print(f"\n[Driver: Terminal] 💻 Виконую команду: '{command}'...")
        try:
            # Запускаємо команду в ізольованій папці
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=15 # Обмеження в 15 секунд, щоб не завис
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"
                
            if not output.strip():
                return "Command executed successfully with no output."
                
            return output[:2000] # Обрізаємо занадто довгий вивід
        except subprocess.TimeoutExpired:
            return "Error: Command execution timed out (limit is 15s)."
        except Exception as e:
            return f"Execution Error: {str(e)}"