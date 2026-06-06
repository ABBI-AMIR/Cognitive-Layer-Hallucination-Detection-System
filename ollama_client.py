import requests
from config.config import Config


class OllamaClient:

    def generate(self, prompt: str) -> str:
        response = requests.post(
            Config.OLLAMA_URL,
            json={
                "model": Config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            }
        )
        return response.json().get("response", "")
