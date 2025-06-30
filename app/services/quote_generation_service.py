import httpx
import structlog
from fastapi import Depends
from textwrap import dedent
from typing import List, Dict, Tuple

from app.core.config import Settings, settings


class QuoteGenerationService:
    def __init__(self, settings: Settings = Depends(lambda: settings)):
        self.settings = settings
        self.api_base_url = "https://openrouter.ai/api/v1"
        self.log = structlog.get_logger(__name__)

    async def _call_openrouter(self, model: str, messages: List[Dict[str, str]]) -> Dict:
        headers = {"Authorization": f"Bearer {self.settings.OPENROUTER_API_KEY}"}
        json_data = {"model": model, "messages": messages}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/chat/completions",
                headers=headers,
                json=json_data,
                timeout=20.0,
            )
            response.raise_for_status()
            return response.json()

    async def generate_quote(self, mood: str) -> Tuple[str, str]:
        """Return a motivational quote text and author."""
        prompt = dedent(
            f"""
            Buat satu kutipan motivasi singkat sesuai suasana hati berikut: {mood}.
            Jika relevan, sertakan nama penulis setelah tanda dash.
            """
        ).strip()

        messages = [{"role": "system", "content": prompt}]

        try:
            data = await self._call_openrouter(
                model=self.settings.GENERATOR_MODEL_NAME,
                messages=messages,
            )
            content = data["choices"][0]["message"]["content"].strip()
            if " - " in content:
                text, author = content.split(" - ", 1)
                return text.strip(), author.strip()
            return content, "Unknown"
        except Exception as e:
            self.log.error("quote_generation_error", error=str(e))
            return "", ""
