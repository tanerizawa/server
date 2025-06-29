import pytest
from app.services.planner_service import PlannerService
from app.schemas.plan import CommunicationTechnique
from app.core.config import Settings


@pytest.mark.asyncio
async def test_get_plan_accepts_four_args(monkeypatch):
    planner = PlannerService(settings=Settings(OPENROUTER_API_KEY="key"))

    async def fake_call(self, model, messages):
        return {"choices": [{"message": {"content": '{"technique": "information"}'}}]}

    monkeypatch.setattr(PlannerService, "_call_openrouter", fake_call)

    plan = await planner.get_plan("hello", ["hi"], "", None, "neutral")
    assert plan.technique == CommunicationTechnique.INFORMATION

