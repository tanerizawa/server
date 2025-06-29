from pydantic import BaseModel, ConfigDict

class ArticleBase(BaseModel):
    title: str
    url: str

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
