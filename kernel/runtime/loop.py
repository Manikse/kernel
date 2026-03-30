import re
from kernel.a2a.protocol import A2AController
from kernel.acl.provider import ACLController
from kernel.unms.memory import UNMSController
from kernel.runtime.planner import CognitivePlanner

class KernelRuntime:
    def __init__(self, acl, memory, drivers: dict):
        self.acl = acl
        self.memory = memory  # Ось наша підключена пам'ять
        self.drivers = drivers
        self.planner = CognitivePlanner(acl)
        self.planner = CognitivePlanner(acl)
        self.a2a = A2AController(acl)  # Підключаємо менеджер агентів

    async def step(self, user_input: str) -> str:
        # 1. Дістаємо історію розмов
        conversation_context = self.memory.get_context_string()
        
        # Передаємо Планувальнику запит + історію
        enriched_input = f"CONTEXT:\n{conversation_context}\n\nCURRENT REQUEST:\n{user_input}"
        
        # ЕТАП 1: ПЛАНУВАННЯ
        tasks = await self.planner.create_plan(enriched_input)
        
        if not tasks:
            return "Kernel Error: Cognitive Planner failed to generate an execution sequence."

        results_summary = []
        
        # ЕТАП 2: ВИКОНАННЯ
        for task in tasks:
            print(f"\n[MK-1 EXEC] Step {task.step_id}: {task.description} [Tool: {task.tool}]")
            
            try:
                if task.tool == "web_search" and "web_search" in self.drivers:
                    task.result = await self.drivers["web_search"].execute(task.description) 
                
                elif task.tool == "terminal" and "terminal" in self.drivers:
                    task.result = self.drivers["terminal"].execute(task.description)
                
                elif task.tool == "file_system" and "file_system" in self.drivers:
                    task.result = self.drivers["file_system"].execute(task.description)
                elif task.tool == "spawn_agent":
                    # Парсимо команду формату "Ім'я | Роль | Задача"
                    parts = task.description.split("|")
                    if len(parts) >= 3:
                        name = parts[0].strip()
                        role = parts[1].strip()
                        prompt = parts[2].strip()
                        task.result = await self.a2a.delegate(name, role, prompt)
                    else:
                        task.result = "FAILED: Invalid spawn_agent format. Use 'Name | Role | Task'."
                
                else:
                    task.result = await self.acl.execute(task.description)
                    
                task.status = "COMPLETED"
                
            except Exception as e:
                task.result = f"CRITICAL FAILURE: {str(e)}"
                task.status = "FAILED"
                
            results_summary.append(f"Step {task.step_id} ({task.tool}) | Status: {task.status}\nData/Output: {task.result}")

        # ЕТАП 3: СИНТЕЗ
        compiled_results = "\n---\n".join(results_summary)
        
        final_prompt = f"""
        PREVIOUS CONVERSATION CONTEXT:
        {conversation_context}
        
        The Founder requested: "{user_input}"
        
        The system executed the following autonomous plan and gathered this raw data:
        {compiled_results}
        
        Based on these raw execution logs and context, provide a clear, professional, and visionary final response to the Founder. 
        """
        
        final_response = await self.acl.execute(final_prompt)
        
        # 4. ЗАПИСУЄМО В ПАМ'ЯТЬ
        self.memory.add_interaction(user_input, final_response)
        
        return final_response