import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from dotenv import load_dotenv

# Імпортуємо твої розробки
from main import ACLController, RealAIProvider, UNMSController, KernelRuntime, FileDriver, WebSearchDriver, TerminalDriver

app = FastAPI(title="Manikse Kernel UI")
load_dotenv()

# Ініціалізація Ядра (ті самі компоненти, що в main.py)
API_KEY = os.getenv("OPENROUTER_API_KEY")
acl = ACLController()
if API_KEY:
    acl.register_provider("real_ai", RealAIProvider(api_key=API_KEY))

memory = UNMSController()
kernel = KernelRuntime(acl, memory, drivers={
    "web_search": WebSearchDriver(),
    "terminal": TerminalDriver(working_dir="./kernel_workspace")
})

# --- UI DESIGN (HTML + CSS + JS) ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VESTASTACK // MK-1</title>
    <style>
        body { background: #121212; color: #fff; font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        /* HEADER - VESTA STYLE */
        #header { padding: 15px 30px; background: #000; border-bottom: 2px solid #00ffcc; color: #fff; font-size: 14px; text-transform: uppercase; letter-spacing: 3px; font-weight: 900; box-shadow: 0 0 10px #00ffcc66; }
        
        /* CHAT WINDOW */
        #chat-window { flex: 1; overflow-y: auto; padding: 30px; display: flex; flex-direction: column; gap: 15px; background: #1a1a1a; }
        
        /* MESSAGE BUBBLES */
        .message { padding: 15px 20px; border-radius: 12px; max-width: 80%; line-height: 1.6; font-size: 15px; position: relative; }
        
        /* FOUNDER (YOU) */
        .founder { align-self: flex-end; background: #fff; color: #000; border-bottom-right-radius: 2px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); font-weight: 500; }
        .founder::after { content: 'Founder'; font-size: 10px; color: #888; position: absolute; top: -18px; right: 5px; text-transform: uppercase; font-weight: bold; }

        /* KERNEL (MK-1) */
        .kernel { align-self: flex-start; background: #2d2d2d; color: #fff; border-bottom-left-radius: 2px; border: 1px solid #444; }
        .kernel::after { content: 'Kernel (MK-1)'; font-size: 10px; color: #00ffcc; position: absolute; top: -18px; left: 5px; text-transform: uppercase; font-weight: bold; }

        /* INPUT AREA */
        #input-area { padding: 25px 30px; background: #000; border-top: 2px solid #00ffcc33; display: flex; gap: 15px; }
        input { flex: 1; background: #222; border: 1px solid #333; color: #fff; padding: 18px; font-size: 16px; border-radius: 8px; outline: none; transition: 0.3s; }
        input:focus { border-color: #00ffcc; box-shadow: 0 0 10px #00ffcc66; background: #282828; }
        
        button { background: #00ffcc; color: #000; border: none; padding: 0 30px; cursor: pointer; font-size: 14px; text-transform: uppercase; font-weight: 900; letter-spacing: 2px; border-radius: 8px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff6; transform: scale(1.03); }
        
        /* SYSTEM STATUS */
        .status-bar { font-size: 11px; color: #888; padding: 10px 30px; background: #080808; text-transform: uppercase; border-bottom: 1px solid #1a1a1a; letter-spacing: 1px; }
        .status-item { margin-right: 20px; }
        .status-item span { color: #00ffcc; font-weight: bold; }
    </style>
</head>
<body>
    <div id="header">MANIKSE KERNEL // COGNITIVE LAYER</div>
    <div class="status-bar">
        <span class="status-item">SYSTEM: <span>v0.2.0 (WEB)</span></span>
        <span class="status-item">ACL: <span>ONLINE</span></span>
        <span class="status-item">MEM: <span>READY</span></span>
    </div>
    <div id="chat-window">
        <div class="message kernel">Greetings, Founder. Systems initialized. I am ready to manage agents, analyze data, or assist in any task needed.</div>
    </div>
    <div id="input-area">
        <input type="text" id="userInput" placeholder="How may I assist you today?" autocomplete="off">
        <button onclick="sendMessage()">PROCESS</button>
    </div>

    <script>
        const input = document.getElementById('userInput');
        chatWindow = document.getElementById('chat-window');

        input.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

        async function sendMessage() {
            const text = input.value.trim();
            if (!text) return;

            addMessage(text, 'founder');
            input.value = '';

            // Надсилаємо на сервер
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                if (!response.ok) throw new Error("Network issues");
                const data = await response.json();
                addMessage(data.response, 'kernel');
            } catch (e) {
                addMessage("Kernel Error: System interrupt detected. Please check your API key and connection.", 'kernel');
            }
        }

        function addMessage(text, type) {
            const div = document.createElement('div');
            div.className = `message ${type}`;
            div.innerText = text;
            chatWindow.appendChild(div);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    # Викликаємо логіку Ядра
    response = await kernel.step(user_message)
    
    return JSONResponse({"response": response})

if __name__ == "__main__":
    # Запускаємо сервер на localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)