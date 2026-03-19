from duckduckgo_search import DDGS
from ddgs import DDGS

class WebSearchDriver:
    def __init__(self):
        self.name = "WebSearch"

    def search(self, query: str, max_results: int = 3) -> str:
        print(f"\n[Driver: WebSearch] 🌐 Здійснюю пошук: '{query}'...")
        try:
            # Використовуємо нову бібліотеку
            results = DDGS().text(query, max_results=max_results)
            # Якщо результатів немає або це не список
            if not results:
                return "No results found."
            
            # Форматуємо результати для LLM
            formatted = "\n".join([f"- {res.get('title', 'No title')}: {res.get('body', 'No body')} ({res.get('href', 'No link')})" for res in results])
            return formatted
        except Exception as e:
            return f"Search Error: {str(e)}"