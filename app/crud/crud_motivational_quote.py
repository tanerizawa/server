from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models.motivational_quote import MotivationalQuote
from app.schemas.motivational_quote import MotivationalQuoteCreate, MotivationalQuoteUpdate

class CRUDMotivationalQuote(CRUDBase[MotivationalQuote, MotivationalQuoteCreate, MotivationalQuoteUpdate]):
    pass

motivational_quote = CRUDMotivationalQuote(MotivationalQuote)
