import requests
import asyncio

class OllamaProvider:
    """Драйвер для автономного локального інтелекту (Ollama)."""
    
    def __init__(self, model="llama3", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = f"{base_url}/api/generate"

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        # Формуємо єдиний контекст для моделі
        full_prompt = f"System Context: {system_prompt}\n\nUser Command: {prompt}" if system_prompt else prompt
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }
        
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: requests.post(self.base_url, json=payload, timeout=120)
            )
            response.raise_for_status()
            return response.json().get("response", "Error: Empty response from Ollama.")
        
        except Exception as e:
            return f"FAILED: Local Edge Error - {str(e)}"