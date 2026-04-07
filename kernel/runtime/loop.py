import re
from kernel.a2a.protocol import A2AController
from kernel.acl.provider import ACLController
from kernel.unms.memory import UNMSController
from kernel.runtime.planner import CognitivePlanner

class KernelRuntime:
    def __init__(self, acl, memory, drivers: dict):
        self.acl = acl
        self.memory = memory
        self.drivers = drivers
        self.planner = CognitivePlanner(acl)
        self.a2a = A2AController(acl)
        
        # ЗАПОБІЖНИК: Максимальна кількість спроб самовиправлення за один запит
        self.max_recoveries = 3 

    def _is_error(self, result: str) -> bool:
        res = str(result).lower()
        if res.startswith("failed:") or res.startswith("critical failure:"):
            return True
            
        error_signatures = [
            "traceback (most recent",
            "syntaxerror:",
            "nameerror:",
            "typeerror:",
            "indentationerror:",
            "command not found",
            "no such file or directory",
            "permission denied",
            "fatal error:"
        ]
        return any(sig in res for sig in error_signatures)

    async def step(self, user_input: str) -> str:
        conversation_context = self.memory.get_context_string()
        enriched_input = f"CONTEXT:\n{conversation_context}\n\nCURRENT REQUEST:\n{user_input}"
        
        tasks = await self.planner.create_plan(enriched_input)
        
        if not tasks:
            return "Kernel Error: Cognitive Planner failed to generate an execution sequence."

        results_summary = []
        step_outputs = {}
        
        current_recoveries = 0 # Лічильник спроб для поточного сеансу
        
        i = 0
        while i < len(tasks):
            task = tasks[i]
            
            # --- DATA PIPING MAGIC ---
            matches = re.findall(r"\{\{STEP_(\d+)_RESULT\}\}", task.description)
            for match in matches:
                step_num = int(match)
                if step_num in step_outputs:
                    task.description = task.description.replace(f"{{{{STEP_{step_num}_RESULT}}}}", step_outputs[step_num])
            # -------------------------

            print(f"\n[ExArchon EXEC] Step {task.step_id}: {task.description[:100]}... [Tool: {task.tool}]")
            
            try:
                if task.tool == "web_search" and "web_search" in self.drivers:
                    task.result = await self.drivers["web_search"].execute(task.description) 
                
                elif task.tool == "terminal" and "terminal" in self.drivers:
                    task.result = self.drivers["terminal"].execute(task.description)
                
                elif task.tool == "file_system" and "file_system" in self.drivers:
                    task.result = self.drivers["file_system"].execute(task.description)
                
                elif task.tool == "spawn_agent" and hasattr(self, 'a2a'):
                    parts = task.description.split("|")
                    if len(parts) >= 3:
                        name, role, prompt = [p.strip() for p in parts[:3]]
                        task.result = await self.a2a.delegate(name, role, prompt)
                    else:
                        task.result = "FAILED: Invalid format."
                else:
                    task.result = await self.acl.execute(task.description)
                    
                task.status = "COMPLETED"
                
            except Exception as e:
                task.result = f"CRITICAL FAILURE: {str(e)}"
                task.status = "FAILED"
                
            step_outputs[task.step_id] = str(task.result)
            results_summary.append(f"Step {task.step_id} ({task.tool}) | Status: {task.status}\nData/Output: {str(task.result)[:200]}...")

            # --- REFLECTION LOOP (SELF-CORRECTION WITH GUARDRAILS) ---
            if self._is_error(task.result):
                if current_recoveries >= self.max_recoveries:
                    # ЗАПОБІЖНИК СПРАЦЮВАВ! Зупиняємо конвеєр.
                    print(f"\n[ExArchon REFLECTION] 🛑 CRITICAL: Maximum recovery attempts ({self.max_recoveries}) reached! Halting execution to prevent infinite loop.")
                    results_summary.append(f"\n[SYSTEM HALT] Execution aborted. Max retries exceeded.")
                    break # Виходимо з циклу
                    
                current_recoveries += 1
                print(f"\n[ExArchon REFLECTION] 🚨 Error detected in Step {task.step_id}! Initiating Recovery Plan (Attempt {current_recoveries}/{self.max_recoveries})...")
                
                recovery_prompt = f"""
                CRITICAL ALERT:
                The previous step failed.
                Attempted Action: {task.description}
                Error Output: {task.result}
                
                Your task is to analyze this error and generate a RECOVERY PLAN to fix it.
                Return ONLY a JSON array with the next steps to fix the problem and continue the main goal. 
                Start the "step_id" numbering from {len(tasks) + 1}.
                """
                
                recovery_tasks = await self.planner.create_plan(recovery_prompt)
                
                if recovery_tasks:
                    print(f"[ExArchon REFLECTION] 🛠️ Recovery Plan injected into queue.")
                    tasks.extend(recovery_tasks)
                else:
                    print(f"[ExArchon REFLECTION] ⚠️ Failed to create Recovery Plan. Stopping execution.")
                    break
            # -----------------------------------------

            i += 1

        compiled_results = "\n---\n".join(results_summary)
        
        final_prompt = f"""
        PREVIOUS CONVERSATION CONTEXT:
        {conversation_context}
        
        The Founder requested: "{user_input}"
        
        The system executed the following autonomous plan and gathered this raw data:
        {compiled_results}
        
        Based on these raw execution logs and context, provide a clear, professional final response.
        If the system had to halt due to maximum retries, clearly report the failure and ask the Founder for manual intervention.
        """
        
        final_response = await self.acl.execute(final_prompt)
        self.memory.add_interaction(user_input, final_response)
        
        return final_response