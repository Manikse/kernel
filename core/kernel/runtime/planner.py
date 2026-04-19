import json
import platform
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
        # --- АВТОВИЗНАЧЕННЯ СЕРЕДОВИЩА ---
        os_name = platform.system()
        if os_name == "Windows":
            env_hint = "You are running on Windows. For the 'terminal' tool, strictly use PowerShell commands (e.g., Get-Date, Get-ChildItem)."
        elif os_name == "Darwin":
            env_hint = "You are running on macOS. For the 'terminal' tool, use standard bash/zsh commands."
        else:
            env_hint = f"You are running on {os_name} (Linux-based). For the 'terminal' tool, use standard bash commands (e.g., date, ls, pwd)."

        # Використовуємо f-строку з подвійними дужками для екранування JSON-формату
        system_prompt = f"""
        You are the ExArchon Cognitive Planner. Break down the user's goal into a logical sequence of actionable tasks.
        
        ENVIRONMENT: {env_hint}
        
        AVAILABLE TOOLS:
        - terminal: Execute raw OS commands.
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
        5. If tool is "web_search", "command" MUST be the exact search query. DO NOT write explanations.
        6. PROBLEM SOLVING: If you need real-time data, write a quick script using 'terminal' tool.
        7. DATA PIPING (CRITICAL): If Step B needs the output of Step A, you MUST use the exact syntax {{{{STEP_A_RESULT}}}} inside Step B's command.

        CORRECT FORMAT EXAMPLE:
        [
            {{"step_id": 1, "tool": "spawn_agent", "command": "DevOps-Master | Senior Linux Admin | Write a script"}},
            {{"step_id": 2, "tool": "file_system", "command": "WRITE script.sh\\n{{{{STEP_1_RESULT}}}}"}}
        ]
        """
        
        raw_response = await self.acl.execute(user_goal, system_prompt=system_prompt)
        
        tasks = []
        try:
            cleaned_response = raw_response.strip().strip('`').removeprefix('json').strip()
            plan_data = json.loads(cleaned_response)
            
            for item in plan_data:
                action_text = item.get("command") or item.get("description", "")
                tasks.append(Task(
                    step_id=item.get("step_id"),
                    description=action_text,
                    tool=item.get("tool", "llm")
                ))
        except json.JSONDecodeError:
            print(f"[ExArchon Planner Error] Failed to parse JSON. Fallback to LLM.")
            tasks.append(Task(1, user_goal, "llm"))
            
        return tasks