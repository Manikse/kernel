import re
from kernel.acl.provider import ACLController
from kernel.unms.memory import UNMSController
from kernel.runtime.planner import CognitivePlanner

class KernelRuntime:
    def __init__(self, acl, memory, drivers: dict):
        self.acl = acl
        self.memory = memory
        self.drivers = drivers
        # Підключаємо наш новий мозок
        self.planner = CognitivePlanner(acl)

    async def step(self, user_input: str) -> str:
        # ЕТАП 1: ПЛАНУВАННЯ
        # Ядро більше не відповідає одразу. Воно створює масив задач.
        tasks = await self.planner.create_plan(user_input)
        
        if not tasks:
            return "Kernel Error: Cognitive Planner failed to generate an execution sequence."

        results_summary = []
        
        # ЕТАП 2: ВИКОНАННЯ (Execution Engine)
        for task in tasks:
            print(f"\n[MK-1 EXEC] Step {task.step_id}: {task.description} [Tool: {task.tool}]")
            
            try:
                # Маршрутизація задач до відповідних драйверів
                if task.tool == "web_search" and "web_search" in self.drivers:
                    # Припускаємо, що у WebSearchDriver є метод пошуку
                    # Якщо він називається інакше, заміни .execute на правильну назву
                    task.result = await self.drivers["web_search"].execute(task.description) 
                
                elif task.tool == "terminal" and "terminal" in self.drivers:
                    task.result = self.drivers["terminal"].execute(task.description)
                
                elif task.tool == "file_system" and "file_system" in self.drivers:
                    # Поки що перенаправляємо файлові операції на базовий LLM, 
                    # якщо драйвер ще не має складних методів
                    task.result = await self.acl.execute(f"File System Action needed: {task.description}")
                
                else:
                    # Fallback: якщо це просто логіка, код або текст - віддаємо головному ШІ
                    task.result = await self.acl.execute(task.description)
                    
                task.status = "COMPLETED"
                
            except Exception as e:
                task.result = f"CRITICAL FAILURE: {str(e)}"
                task.status = "FAILED"
                
            # Збираємо логи виконання в один масив
            results_summary.append(f"Step {task.step_id} ({task.tool}) | Status: {task.status}\nData/Output: {task.result}")

        # ЕТАП 3: СИНТЕЗ
        # Згодовуємо всі сирі дані від драйверів назад у ШІ, щоб він зробив гарний звіт для тебе
        compiled_results = "\n---\n".join(results_summary)
        
        final_prompt = f"""
        The Founder requested: "{user_input}"
        
        The system executed the following autonomous plan and gathered this raw data:
        {compiled_results}
        
        Based on these raw execution logs, provide a clear, professional, and visionary final response to the Founder. 
        If the tools failed, explain why. If they succeeded, present the final output beautifully. 
        Do not list the steps mechanically unless it adds value.
        """
        
        final_response = await self.acl.execute(final_prompt)
        return final_response