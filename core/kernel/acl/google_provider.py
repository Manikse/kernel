import google.generativeai as genai
import asyncio

class GoogleProvider:
    """Драйвер для хмарного інтелекту (Google Gemini)."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        # Формуємо контекст
        full_prompt = f"System Instruction: {system_prompt}\n\nUser: {prompt}" if system_prompt else prompt
        
        try:
            # Запускаємо в окремому потоці, щоб не блокувати асинхронний цикл
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                self.model.generate_content, 
                full_prompt
            )
            return response.text
        except Exception as e:
            # Якщо ліміт або немає інтернету — повертаємо спеціальний маркер помилки
            return f"FAILED: Google Cloud Error - {str(e)}"