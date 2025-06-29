import httpx
import json
import structlog
from typing import List, Dict, Optional
from textwrap import dedent

from fastapi import Depends
from app.core.config import Settings, settings
from app.schemas.plan import CommunicationTechnique, ConversationPlan
from app.models.user_profile import UserProfile  # pastikan path ini valid

class PlannerService:
    def __init__(self, settings: Settings = Depends(lambda: settings)):
        self.settings = settings
        self.api_base_url = "https://openrouter.ai/api/v1"
        self.log = structlog.get_logger(__name__)

    async def _call_openrouter(self, model: str, messages: List[Dict[str, str]]) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": self.settings.APP_SITE_URL,
            "X-Title": self.settings.APP_NAME,
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
                timeout=20.0
            )
            response.raise_for_status()
            return response.json()

    async def get_plan(
            self,
            user_message: str,
            chat_history: List[str],
            latest_journal: str,
            user_profile: Optional[UserProfile],
            emotion_label: str,
    ) -> ConversationPlan:
        self.log.info("planning_conversation", user_message=user_message)

        # === KONTEKS JANGKA PANJANG (Profil Pengguna) ===
        profile_summary = "Profil pengguna belum dianalisis."
        if user_profile:
            emerging = user_profile.emerging_themes or {}
            themes_str = ", ".join(
                f"{k} ({v:.0%})" for k, v in emerging.items()
            ) if emerging else "Tidak tersedia"
            sentiment = user_profile.sentiment_trend or "Tidak tersedia"
            profile_summary = f"""
            - Tema yang sering muncul dalam hidupnya: {themes_str}
            - Tren emosionalnya akhir-akhir ini: {sentiment}
            """

        # === KONTEKS JANGKA PENDEK (Percakapan & Jurnal) ===
        history_str = "\n".join(chat_history[-5:])  # 5 pesan terakhir

        available_techniques = ", ".join(
            f"'{t.value}'" for t in CommunicationTechnique if t != CommunicationTechnique.UNKNOWN
        )

        prompt = dedent(f"""
            Anda adalah konselor perencana untuk Dear. Analisis pesan pengguna berdasarkan KONTEKS LENGKAP di bawah ini, kemudian pilih SATU teknik komunikasi yang paling sesuai.

            --- KONTEKS JANGKA PANJANG (Hasil Pembelajaran AI) ---
            {profile_summary}
            ----------------------------------------------------

            --- KONTEKS JANGKA PENDEK ---
            Entri jurnal terbaru pengguna: {latest_journal or 'Tidak ada'}
            Riwayat percakapan sesi ini:
            {history_str}
            Pesan terbaru pengguna: {user_message}
            ----------------------------------------------------

            Tugas Anda: Pilih SATU teknik dari daftar berikut: {available_techniques}

            Balas HANYA dengan objek JSON sederhana seperti {{"technique": "<name>"}}.
        """).strip()

        messages = [{"role": "system", "content": prompt}]

        try:
            data = await self._call_openrouter(self.settings.PLANNER_MODEL_NAME, messages)
            choices = data.get("choices", [])
            if not choices:
                raise ValueError("No choices returned by OpenRouter.")

            content = choices[0].get("message", {}).get("content", "").strip()
            self.log.debug("planner_response_content", content=repr(content))

            # Bersihkan jika response dibungkus dalam blok kode Markdown
            if content.startswith("```json"):
                content = content[len("```json"):].strip()
            if content.endswith("```"):
                content = content[:-3].strip()

            if not content:
                raise ValueError("Empty response content.")

            plan_data = json.loads(content)

            if (
                    "technique" not in plan_data
                    or plan_data["technique"] not in [t.value for t in CommunicationTechnique]
            ):
                raise ValueError(f"Invalid technique returned: {plan_data.get('technique')}")

            return ConversationPlan(**plan_data)

        except json.JSONDecodeError as e:
            self.log.error("planner_service_json_error", error=str(e), raw_response=content)
        except Exception as e:
            self.log.error("planner_service_error", error=str(e))

        return ConversationPlan(technique=CommunicationTechnique.UNKNOWN)
