import json
from typing import List

class Task:
    def __init__(self, step_id: int, description: str, tool: str = "llm"):
        self.step_id = step_id
        self.description = description
        self.tool = tool  
        self.status = "PENDING"
        self.result = None

    def __repr__(self):
        return f"[Step {self.step_id} | Tool: {self.tool}] {self.description}"

class CognitivePlanner:
    def __init__(self, acl):
        self.acl = acl

    async def create_plan(self, user_goal: str) -> List[Task]:
        # ХАК: Змінено ключі в JSON, щоб ШІ писав КОД, а не текст
        system_prompt = """
        You are the MK-1 Cognitive Planner. Break down the user's goal into a logical sequence of actionable tasks.
        
        AVAILABLE TOOLS:
        - terminal: Execute raw OS commands (PowerShell/CMD).
        - file_system: Read or write files (WRITE filename.ext\n[content]).
        - web_search: Search the internet.
        - spawn_agent: Create a specialized sub-agent to do complex thinking, writing, or coding.
        - llm: General reasoning.

        CRITICAL RULES:
        1. Return ONLY a valid JSON array. No markdown, no explanations.
        2. Use exact keys: "step_id", "tool", "command".
        3. If tool is "spawn_agent", the "command" MUST strictly follow this format:
           AgentName | AgentRole | Task to perform
        4. If tool is "file_system", "command" MUST follow format: "WRITE filename.ext\n[content]" or "READ filename.ext".
        5. If tool is "web_search", "command" MUST be the exact search query (e.g., "latest AI news 2026"). DO NOT write explanations.
        6. PROBLEM SOLVING: If you need real-time data (like current weather or stock prices) and standard web_search might not give an exact number in the snippet, write a quick Python script using 'terminal' tool (e.g., using curl, requests, or public APIs like 'curl wttr.in/Bratislava?format=3') to get the data directly.

        CORRECT FORMAT EXAMPLE:
        [
            {"step_id": 1, "tool": "web_search", "command": "Python 3.13 release notes"},
            {"step_id": 2, "tool": "file_system", "command": "WRITE notes.txt\n[summarized data]"}
        ]
        """
        
        raw_response = await self.acl.execute(user_goal, system_prompt=system_prompt)
        
        tasks = []
        try:
            cleaned_response = raw_response.strip().strip('`').removeprefix('json').strip()
            plan_data = json.loads(cleaned_response)
            
            for item in plan_data:
                # Беремо поле command (або description, якщо ШІ все ж помилиться)
                action_text = item.get("command") or item.get("description", "")
                tasks.append(Task(
                    step_id=item.get("step_id"),
                    description=action_text,
                    tool=item.get("tool", "llm")
                ))
        except json.JSONDecodeError:
            print(f"[MK-1 Planner Error] Failed to parse JSON. Fallback to LLM.")
            tasks.append(Task(1, user_goal, "llm"))
            
        return tasks