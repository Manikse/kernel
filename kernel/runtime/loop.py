import re
from kernel.acl.provider import ACLController
from kernel.unms.memory import UNMSController

class KernelRuntime:
    """
    The main execution loop of the Kernel. 
    Intercepts tools: WebSearch and Terminal.
    """
    def __init__(self, acl: ACLController, memory: UNMSController, drivers: dict = None):
        self.acl = acl
        self.memory = memory
        self.drivers = drivers or {}
        self.is_active = True

    async def step(self, user_input: str) -> str:
        # 1. Orient
        self.memory.commit(user_input, role="user")
        full_prompt = f"Context:\n{self.memory.get_context()}\n\nAssistant:"

        # 2. Decide
        response = await self.acl.execute(full_prompt)

        # 3. Act - Шукаємо команди
        search_match = re.search(r"\[SEARCH:\s*(.*?)\]", response)
        exec_match = re.search(r"\[EXECUTE:\s*(.*?)\]", response)
        
        # Обробка SEARCH
        if search_match and "web_search" in self.drivers:
            query = search_match.group(1)
            results = self.drivers["web_search"].search(query)
            self.memory.commit(response, role="assistant")
            sys_msg = f"[SYSTEM: Search Results for '{query}']\n{results}\nAnalyze this and answer the user. DO NOT output another tool command."
            self.memory.commit(sys_msg, role="system")
            
            print("[Kernel] Аналізую дані з інтернету...")
            final_resp = await self.acl.execute(f"Context:\n{self.memory.get_context()}\n\nAssistant:")
            self.memory.commit(final_resp, role="assistant")
            return final_resp

        # Обробка EXECUTE
        elif exec_match and "terminal" in self.drivers:
            command = exec_match.group(1)
            results = self.drivers["terminal"].execute(command)
            self.memory.commit(response, role="assistant")
            sys_msg = f"[SYSTEM: Execution Output for '{command}']\n{results}\nTell the user the result. DO NOT output another tool command."
            self.memory.commit(sys_msg, role="system")
            
            print("[Kernel] Аналізую результати виконання терміналу...")
            final_resp = await self.acl.execute(f"Context:\n{self.memory.get_context()}\n\nAssistant:")
            self.memory.commit(final_resp, role="assistant")
            return final_resp

        # Якщо команд немає - просто відповідаємо
        self.memory.commit(response, role="assistant")
        return response