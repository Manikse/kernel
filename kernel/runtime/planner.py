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
        - file_system: Read, write, or modify files.
        - llm: General reasoning or text generation.

        CRITICAL RULES:
        1. Return ONLY a valid JSON array. No markdown, no explanations.
        2. Use the exact keys: "step_id", "tool", "command".
        3. If tool is "terminal", the "command" field MUST contain ONLY the RAW COMMAND to execute. DO NOT write human explanations!

        CORRECT FORMAT EXAMPLE:
        [
            {"step_id": 1, "tool": "terminal", "command": "echo print(100 * 5) > founder_test.py"},
            {"step_id": 2, "tool": "terminal", "command": "echo print('MK-1 Terminal is online') >> founder_test.py"},
            {"step_id": 3, "tool": "terminal", "command": "python founder_test.py"}
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