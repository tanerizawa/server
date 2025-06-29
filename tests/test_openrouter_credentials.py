import pytest
import httpx
from app.services.planner_service import PlannerService
from app.services.generator_service import GeneratorService
from app.schemas.plan import CommunicationTechnique, ConversationPlan
from app.core.config import Settings


@pytest.mark.asyncio
@pytest.mark.parametrize("api_key", [None, "bad-key"])
async def test_services_handle_invalid_credentials(monkeypatch, api_key):
    planner = PlannerService(settings=Settings(OPENROUTER_API_KEY=api_key))
    generator = GeneratorService(settings=Settings(OPENROUTER_API_KEY=api_key))

    async def raise_error(self, model, messages):
        request = httpx.Request("POST", "https://openrouter.ai")
        response = httpx.Response(status_code=401, request=request)
        raise httpx.HTTPStatusError("Unauthorized", request=request, response=response)

    monkeypatch.setattr(PlannerService, "_call_openrouter", raise_error)
    monkeypatch.setattr(GeneratorService, "_call_openrouter", raise_error)

    plan = await planner.get_plan("hi", [], "", None, "neutral")
    assert plan.technique == CommunicationTechnique.UNKNOWN

    result = await generator.generate_response(plan, [], None)
    assert "listen" in result.lower()

