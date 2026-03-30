import asyncio

class A2AController:
    """
    Протокол Agent-to-Agent. 
    Дозволяє Ядру (MK-1) створювати спеціалізованих підлеглих агентів для виконання задач.
    """
    def __init__(self, acl):
        self.acl = acl

    async def delegate(self, agent_name: str, role: str, task: str) -> str:
        print(f"\n[A2A Protocol] 🤖 Spawning Sub-Agent '{agent_name}'...")
        print(f"[A2A Protocol] 🎯 Role: {role}")
        
        system_prompt = f"""
        You are an autonomous sub-agent operating under the MK-1 Kernel.
        Your Name: {agent_name}
        Your Role: {role}
        
        Your objective is to complete the task assigned by the Kernel. 
        Focus ONLY on your specific role. Return the final, high-quality result.
        """
        
        result = await self.acl.execute(task, system_prompt=system_prompt)
        
        return f"SUCCESS: Sub-Agent '{agent_name}' completed the task.\nResult:\n{result}"