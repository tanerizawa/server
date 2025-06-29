import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.generator_service import GeneratorService


class DummyTechnique:
    def __init__(self, value: str):
        self.value = value


class DummyPlan:
    def __init__(self, technique: str):
        self.technique = DummyTechnique(technique)

@pytest.mark.asyncio
async def test_generate_response_no_duplicate(monkeypatch):
    captured = {}

    async def fake_call(self, model, messages):
        captured['messages'] = messages
        return {"choices": [{"message": {"content": "ok"}}]}

    monkeypatch.setattr(GeneratorService, "_call_openrouter", fake_call)

    plan = DummyPlan("information")
    history = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi"},
        {"role": "user", "content": "how are you?"},
    ]

    from app.core.config import settings as app_settings
    service = GeneratorService(settings=app_settings)
    response = await service.generate_response(plan, history, "neutral")

    assert response == "ok"
    # first message is the system prompt
    assert captured['messages'][1:] == history
    # ensure no duplicate of the latest user message
    assert len(captured['messages']) == len(history) + 1
    assert "how are you?" in captured['messages'][0]['content']
