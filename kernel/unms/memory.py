import time
from typing import List, Dict, Optional

class MemoryEntry:
    """A single unit of memory with metadata."""
    def __init__(self, content: str, role: str, importance: int = 1):
        self.content = content
        self.role = role  # 'user', 'assistant', or 'system'
        self.timestamp = time.time()
        self.importance = importance # From 1 to 10

class UNMSController:
    """
    Unified Neural Memory System (UNMS).
    Зараз працює як Short-Term Memory (Контекстне вікно розмови).
    """
    def __init__(self, max_history=10):
        # Зберігаємо останні 10 повідомлень (щоб не перевантажити контекст)
        self.history = []
        self.max_history = max_history

    def add_interaction(self, user_query: str, kernel_response: str):
        self.history.append({"role": "user", "content": user_query})
        self.history.append({"role": "assistant", "content": kernel_response})
        
        # Якщо історія занадто довга, видаляємо найстаріші повідомлення
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-(self.max_history * 2):]

    def get_context_string(self) -> str:
        if not self.history:
            return "No previous conversation history."
        
        context_lines = []
        for msg in self.history:
            speaker = "Founder" if msg["role"] == "user" else "ExArchon"
            context_lines.append(f"{speaker}: {msg['content']}")
            
        return "\n".join(context_lines)