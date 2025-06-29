import pytest
from datetime import datetime, timedelta

from app.services.music_keyword_service import MusicKeywordService
from app.core.config import Settings
from app.models.journal import Journal


@pytest.mark.asyncio
async def test_generate_keyword_uses_latest_journals(monkeypatch):
    captured = {}

    async def fake_call(self, model, messages):
        captured['messages'] = messages
        return {"choices": [{"message": {"content": "lofi"}}]}

    monkeypatch.setattr(MusicKeywordService, "_call_openrouter", fake_call)

    service = MusicKeywordService(settings=Settings(OPENROUTER_API_KEY="key"))

    journals = [
        Journal(content=f"j{i}", created_at=datetime.utcnow() - timedelta(days=i))
        for i in range(6)
    ]

    result = await service.generate_keyword(journals)

    assert result == "lofi"
    system_prompt = captured['messages'][0]['content']
    assert "j5" not in system_prompt  # oldest excluded
    for i in range(5):
        assert f"j{i}" in system_prompt
