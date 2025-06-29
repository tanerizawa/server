from enum import Enum
from pydantic import BaseModel, Field

class CommunicationTechnique(str, Enum):
    """Enumeration of communication techniques Dear can apply."""

    SOCIAL_GREETING = "social_greeting"
    PROBING = "probing"
    VALIDATION = "validation"
    EMPATHETIC = "empathetic"
    REFLECTION = "reflection"
    SUMMARIZING = "summarizing"
    CLARIFYING = "clarifying"
    INFORMATION = "information"
    # Fallback option when the planner cannot determine the technique
    UNKNOWN = "unknown"

class ConversationPlan(BaseModel):
    technique: CommunicationTechnique = Field(..., description="The communication technique chosen by the planner AI.")
