"""Utilities for generating a music keyword suggestion."""

import httpx
import structlog
from typing import List, Dict
from textwrap import dedent

from fastapi import Depends

from app.core.config import Settings, settings
from app.models.journal import Journal


class MusicKeywordService:
    def __init__(self, settings: Settings = Depends(lambda: settings)):
        self.settings = settings
        self.api_base_url = "https://openrouter.ai/api/v1"
        self.log = structlog.get_logger(__name__)

    async def _call_openrouter(self, model: str, messages: List[Dict[str, str]]) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.settings.OPENROUTER_API_KEY}"
        }
        json_data = {
            "model": model,
            "messages": messages
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base_url}/chat/completions",
                headers=headers,
                json=json_data,
                timeout=20.0,
            )
            response.raise_for_status()
            return response.json()

    async def generate_keyword(self, journals: List[Journal]) -> str:
        """Generate a music keyword based on the latest journal entries."""
        sorted_journals = sorted(
            journals,
            key=lambda j: getattr(j, "created_at", 0),
            reverse=True,
        )
        combined = "\n".join(j.content for j in sorted_journals[:5])
        prompt = dedent(
            f"""
            Berdasarkan entri jurnal berikut, sarankan satu judul lagu atau kata kunci yang mewakili suasana hati penulis. Balas dengan singkat tanpa penjelasan.
            {combined}
            """
        ).strip()

        messages = [{"role": "system", "content": prompt}]

        try:
            data = await self._call_openrouter(
                model=self.settings.GENERATOR_MODEL_NAME,
                messages=messages,
            )
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            self.log.error("music_keyword_service_error", error=str(e))
            return ""
