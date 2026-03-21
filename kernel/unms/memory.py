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
    The brain's storage. Manages where data goes based on its 'age' and 'relevance'.
    """
    def __init__(self):
        # Hot Layer: Current conversation (RAM)
        self.working_memory: List[MemoryEntry] = []
        
        # Warm Layer: Recent history (to be moved to Vector DB later)
        self.episodic_buffer: List[MemoryEntry] = []
        
        # Cold Layer: Permanent facts (Knowledge Graph/Vector DB)
        self.semantic_core: Dict[str, str] = {}

    def commit(self, content: str, role: str):
        """Adds new information to the Working Memory."""
        entry = MemoryEntry(content, role)
        self.working_memory.append(entry)
        
        # If Working Memory is too large, trigger consolidation
        if len(self.working_memory) > 10:
            self._consolidate()

    def _consolidate(self):
        """
        The 'Sleep Cycle' logic. 
        Moves old working memory to the episodic buffer.
        """
        print("[Kernel] Consolidation triggered: Moving data to Warm Storage...")
        to_move = self.working_memory[:5]
        self.episodic_buffer.extend(to_move)
        self.working_memory = self.working_memory[5:]

    def get_context(self) -> str:
        """Returns the current relevant context for the LLM."""
        return "\n".join([f"{e.role}: {e.content}" for e in self.working_memory])