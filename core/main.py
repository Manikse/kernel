import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv
from abc import ABC, abstractmethod

# НОВІ ІМПОРТИ ДЛЯ GOOGLE GEMINI
from google import genai
from google.genai import types

# Твої власні імпорти 
from drivers.terminal import TerminalDriver
from drivers.web_search import WebSearchDriver
from drivers.file_system import FileSystemDriver
from kernel.unms.memory import UNMSController
from kernel.runtime.loop import KernelRuntime

# БЕЗПЕЧНИЙ ФІКС КОДУВАННЯ
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# --- ACL SECTION ---
class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        pass

# НОВИЙ ПРОВАЙДЕР GOOGLE (Без лімітів на токени!)
class GoogleProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        KERNEL_MANIFESTO = """
        You are the ExArchon. 
        You are created by Manikse.
        Manikse is a visionary founder building the future of AI.
        You are a Cognitive Operating System Layer.
        Your architecture consists of three core components: 
        - ACL (Agent Control Layer for Reasoning)
        - UNMS (Unified Neural Memory System)
        - A2A (Agent-to-Agent Protocol)
        Your purpose is to manage autonomous agents and interact with the physical world via Drivers.
        Respond in a professional, efficient, and visionary tone.
        Always respond in the same language as the Founder. Maintain a visionary but adaptive tone.
        """
        
        # Налаштовуємо системний промпт для Gemini
        config = types.GenerateContentConfig(
            system_instruction=system_prompt or KERNEL_MANIFESTO,
        )
        
        try:
            # Асинхронний виклик Gemini API
            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            return f"Kernel Error (Google): {str(e)}"

class ACLController:
    def __init__(self):
        self.providers = {}
        self.default_provider = "real_ai"

    def register_provider(self, name: str, provider: LLMProvider):
        self.providers[name] = provider

    async def execute(self, prompt: str, provider_name: str = None, system_prompt: str = "") -> str:
        target = provider_name or self.default_provider
        if target not in self.providers:
            return "Error: No provider registered."
        return await self.providers[target].generate(prompt, system_prompt=system_prompt)


# --- ГЛОБАЛЬНЕ ЯДРО (Для доступу через API) ---
global_kernel = None


# --- BACKGROUND DAEMON WORKER ---
async def daemon_worker():
    """Фонова служба ExArchon для API сервера."""
    print("[DAEMON] Worker initialized and sleeping in background...")
    while True:
        await asyncio.sleep(3600)  
        print("[DAEMON] Executing scheduled background task...")
        bg_task = "SYSTEM TASK: Зроби запис у файл daemon_status.log про те, що система перевірена у фоновому режимі і працює стабільно. Додай поточний час та дату. Return a brief status summary."
        
        try:
            if global_kernel:
                await global_kernel.step(bg_task)
                print("[DAEMON] Background task completed successfully.")
        except Exception as e:
            print(f"[DAEMON] Error: {e}")


# --- ЖИТТЄВИЙ ЦИКЛ СЕРВЕРА ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    global global_kernel
    
    print("🛰️ Initializing ExArchon Core Systems...")
    load_dotenv()
    
    # ТЕПЕР ШУКАЄМО КЛЮЧ GOOGLE
    GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
    
    acl = ACLController()
    if GOOGLE_KEY:
        acl.register_provider("real_ai", GoogleProvider(api_key=GOOGLE_KEY))
        print("[SYSTEM] ACL Layer: ONLINE (Google Gemini API)")
    else:
        print("[SYSTEM] ACL Layer: OFFLINE (Missing GOOGLE_API_KEY in .env)")
        
    memory = UNMSController()
    
    file_system = FileSystemDriver(working_dir="./kernel_workspace")
    web_search = WebSearchDriver()
    terminal = TerminalDriver(working_dir="./kernel_workspace")
    
    global_kernel = KernelRuntime(acl, memory, drivers={
        "web_search": web_search, 
        "terminal": terminal,
        "file_system": file_system
    })
    
    print("[SYSTEM] Drivers active: Terminal, WebSearch, FileSystem")
    
    daemon_task = asyncio.create_task(daemon_worker())
    
    print("🚀 EXARCHON Nexus API is ready and listening!")
    
    yield 
    
    print("🛑 Shutting down ExArchon Core...")
    daemon_task.cancel()


# --- API SETUP ---
app = FastAPI(
    title="EXARCHON Nexus",
    description="The Headless Cognitive Operating System API",
    version="0.4.0",
    lifespan=lifespan 
)

class ExecuteRequest(BaseModel):
    task: str
    session_id: str = "founder_terminal_alpha" 

class ExecuteResponse(BaseModel):
    status: str
    result: str

@app.get("/")
async def root():
    return {"status": "online", "message": "EXARCHON Core is running."}

@app.post("/execute", response_model=ExecuteResponse)
async def execute_task(req: ExecuteRequest):
    if not global_kernel:
        raise HTTPException(status_code=500, detail="Kernel not initialized.")
    
    print(f"[*] Прийнято нове мережеве завдання: {req.task}")
    try:
        result = await global_kernel.step(req.task, req.session_id)
        return ExecuteResponse(status="success", result=result)
    except Exception as e:
        print(f"[ERROR] Помилка виконання: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)