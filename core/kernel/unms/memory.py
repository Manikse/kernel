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
    Мульти-сесійна пам'ять (Stateful API Memory).
    """
    def __init__(self, max_history=10):
        # Зберігаємо історії розмов ДЛЯ РІЗНИХ СЕСІЙ
        # Формат: {"session_id": [{"role": "user", "content": "..."}]}
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        self.max_history = max_history

    def _get_or_create_session(self, session_id: str) -> List[Dict[str, str]]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def add_interaction(self, session_id: str, user_query: str, kernel_response: str):
        history = self._get_or_create_session(session_id)
        
        history.append({"role": "user", "content": user_query})
        history.append({"role": "assistant", "content": kernel_response})
        
        # Якщо історія конкретної сесії занадто довга, обрізаємо старі
        if len(history) > self.max_history * 2:
            self.sessions[session_id] = history[-(self.max_history * 2):]

    def get_context_string(self, session_id: str) -> str:
        history = self.sessions.get(session_id, [])
        if not history:
            return "No previous conversation history."
        
        context_lines = []
        for msg in history:
            speaker = "Founder" if msg["role"] == "user" else "ExArchon"
            context_lines.append(f"{speaker}: {msg['content']}")
            
        return "\n".join(context_lines)