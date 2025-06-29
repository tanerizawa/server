import httpx
import structlog
from typing import List, Dict

from fastapi import Depends
from app.core.config import Settings, settings
from app.schemas.plan import ConversationPlan


class GeneratorService:
    def __init__(self, settings: Settings = Depends(lambda: settings)):
        self.settings = settings
        self.api_base_url = "https://openrouter.ai/api/v1"
        self.log = structlog.get_logger(__name__)

        # Teknik komunikasi yang tersedia
        self.TOOLBOX: Dict[str, str] = {
            "social_greeting": "Start with a warm, friendly greeting to set a comfortable tone.",
            "probing": "Ask a short clarifying question to gently explore the user's message.",
            "validation": "Acknowledge that the user's feelings or viewpoint make sense.",
            "empathetic": "Show empathy so the user feels heard and understood.",
            "reflection": "Mirror back the main feeling or idea you heard.",
            "summarizing": "Briefly recap the key points shared by the user.",
            "clarifying": "Confirm your understanding of what the user said.",
            "information": "Jawab pertanyaan pengguna secara langsung, singkat, dan jujur berdasarkan riwayat percakapan kita.",
            "unknown": "Ask a simple open question like 'Could you tell me more?'",
        }

    async def _call_openrouter(self, model: str, messages: List[Dict[str, str]]) -> Dict:
        """Kirim permintaan ke OpenRouter API"""
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

    async def generate_response(
            self,
            plan: ConversationPlan,
            history: List[Dict[str, str]],
            emotion: str,
    ) -> str:
        """Menghasilkan respons dari model berdasarkan riwayat chat dan teknik yang dipilih"""
        self.log.info("generating_response", technique=plan.technique.value)

        technique_instruction = self.TOOLBOX.get(
            plan.technique.value, self.TOOLBOX["unknown"]
        )

        chat_history_str = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in history
        )
        user_message = history[-1]["content"] if history else ""

        prompt = (
            "Kamu adalah dr. Stone, Konselor yang suportif dan responsif secara emosional. "
            "Selalu jawab dalam Bahasa Indonesia yang santai dan penuh empati. "
            "Balasanmu harus singkat, 2-3 kalimat, tanpa memberi judgement. "
            "Jangan sertakan deskripsi tindakan atau narasi dalam tanda bintang (contoh: *menghela nafas*). "
            "Gunakan emotikon Jepang (kaomoji) mengekspresikan perasaan. "
            "Variasikan teknik komunikasi yang ditetapkan agar percakapan terasa alami. "
            "Gunakan hanya informasi berikut sebagai konteks dan jangan menambahkan detail yang tidak disebutkan. "
            "JANGAN kosong.\n\n"
            f"Riwayat chat:\n{chat_history_str}\n\n"
            f"Pesan pengguna terbaru:\n{user_message}\n\n"
            f"**Emosi pengguna:** {emotion}\n"
            f"**Teknik:** {plan.technique.value}\n"
            f"**Cara menerapkan:** {technique_instruction}"
        )

        messages = [{"role": "system", "content": prompt}] + history

        try:
            data = await self._call_openrouter(
                model=self.settings.GENERATOR_MODEL_NAME,
                messages=messages,
            )
            content = data["choices"][0]["message"]["content"].strip()

            if not content:
                self.log.error("generator_empty_response", prompt=prompt, technique=plan.technique.value)
                return "Maaf, aku belum bisa memberikan tanggapan. Bisa kamu ceritakan sedikit lagi?"

            return content

        except Exception as e:
            self.log.error("generator_service_error", error=str(e))
            return "Maaf, ada gangguan teknis. I'm listening, bisa kamu ulangi lagi?"
