from pydantic import BaseModel, ConfigDict

class MotivationalQuoteBase(BaseModel):
    text: str
    author: str

class MotivationalQuoteCreate(MotivationalQuoteBase):
    pass

class MotivationalQuoteUpdate(MotivationalQuoteBase):
    pass

class MotivationalQuote(MotivationalQuoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
